from flask import Flask, render_template, request, session, jsonify
import threading
import json
import os
from core import llm, prompts, stt

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session storage

# 🔹 Model List (Easily Updatable)
AVAILABLE_MODELS = ["deepseek/deepseek-r1:free", "mistralai/mistral-small-3.1-24b-instruct:free", "google/gemma-3-4b-it:free"]


# Load Faster Whisper Transcriber
transcriber = stt.WhisperTranscriber(model_size="base")  # Change model size if needed

# Ensure the 'audio_files' directory exists
os.makedirs("audio_files", exist_ok=True)


@app.route("/setup", methods=["POST"])
def setup():
    data = json.loads(request.data)
    company, job_title, job_description = prompts.interview_templates()
    print("Company:" + data["company"])
    if len(data["company"]) < 2:
        session["company"] = company
    else:
        session["company"] = data["company"]

    if len(data["position"]) < 2:
        session["position"] = job_title
    else:
        session["position"] = data["position"]

    if len(data["description"]) < 2:
        session["description"]  = job_description
    else:
        session["description"] = data["description"]

    print("-----Interview Info----\n" + "Company:" + session["company"] + "\n" + "Position:" + session["position"] + "\n" )
    session["conversation"] = [{"role": "system", "content": prompts.get_interview_prompt(session)}]
    return {"status": "ok"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get-models")
def get_models():
    """Send model list to frontend"""
    return jsonify(AVAILABLE_MODELS)

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

@app.route("/chat", methods=["POST"])
def chat():
    user_message = json.loads(request.data)["message"]
    response = llm.chat_with_ai(user_message, session)
    return {"response": response}

if __name__ == "__main__":
    app.run(debug=True)
