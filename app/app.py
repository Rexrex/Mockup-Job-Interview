from flask import Flask, render_template, request, session, jsonify, send_file
import threading
import json
import os
from core import llm, prompts, azure_stt

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session storage

# 🔹 Model List (Easily Updatable)
AVAILABLE_MODELS = ["deepseek/deepseek-r1:free", "mistralai/mistral-small-3.1-24b-instruct:free", "google/gemma-3-4b-it:free"]


# Load Faster Whisper Transcriber
transcriber = azure_stt.Transcriber()  # Change model size if needed

# Ensure the 'audio_files' directory exists
os.makedirs("audio_files", exist_ok=True)


@app.route("/setup", methods=["POST"])
def setup():
    """Retrieve setup data and store it in session."""
    data = json.loads(request.data)

    # Default values if user input is empty
    default_company, default_job_title, default_job_description = prompts.get_interview_templates()

    session["company"] = data["company"] if len(data["company"]) > 1 else default_company
    session["position"] = data["position"] if len(data["position"]) > 1 else default_job_title
    session["description"] = data["description"] if len(data["description"]) > 1 else default_job_description

    print(f"----- Interview Setup -----\nCompany: {session['company']}\nPosition: {session['position']}")

    # Store initial system message for the interview
    session["conversation"] = [{"role": "system", "content": prompts.get_interview_prompt(session)}]

    return {"status": "ok"}

@app.route("/")
def setup_page():
    return render_template("index.html")

@app.route("/get-models")
def get_models():
    """Send model list to frontend"""
    return jsonify(AVAILABLE_MODELS)

@app.route('/interview')
def interview():
    return render_template("interview.html")

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    audio_path = os.path.join("audio_files", audio_file.filename)
    audio_file.save(audio_path)

    # Transcribe the saved audio
    transcription = transcriber.transcribe_audio(audio_path)

    # Clean up (remove file after processing)
    os.remove(audio_path)

    return jsonify({"transcription": transcription})


@app.route("/synthesize", methods=["POST"])
def synthesize_speech():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    audio_file = transcriber.synthesize_speech_azure(text)
    return send_file(audio_file, mimetype="audio/wav")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = json.loads(request.data)["message"]
    response = llm.chat_with_ai(user_message, session)
    return {"response": response}

if __name__ == "__main__":
    app.run(debug=True)
