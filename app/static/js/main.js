let mediaRecorder;
let audioChunks = [];
let isListening = false; // Controls user audio
let isAiSpeaking = true; // Controls AI voice

document.addEventListener("DOMContentLoaded", async function () {
    await loadModels(); // Load available AI models
});

// Load AI models into the dropdown
async function loadModels() {
    let response = await fetch("/get-models");
    let models = await response.json();
    let modelSelect = document.getElementById("ai-model");
    modelSelect.innerHTML = models.map(m => `<option value="${m}">${m}</option>`).join("");
}

// Handle interview setup
async function startInterview() {
    let interviewData = {
        company: document.getElementById("company-name").value.trim(),
        position: document.getElementById("job-position").value.trim(),
        description: document.getElementById("job-description").value.trim(),
        model: document.getElementById("ai-model").value
    };

    let response = await fetch("/setup", {
        method: "POST",
        body: JSON.stringify(interviewData),
        headers: { "Content-Type": "application/json" }
    });

    let result = await response.json();
    if (result.status === "ok") {
        window.location.href = "/interview";
    } else {
        alert("Error setting up interview.");
    }
}

// Toggle user microphone
async function toggleMic() {
    isListening = !isListening;
    document.getElementById("micButton").textContent = isListening ? "Mute Mic" : "Unmute Mic";

    if (isListening) {
        startListening();
    } else {
        stopListening();
    }
}

// Start continuous transcription
async function startListening() {
    let stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        let audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        let formData = new FormData();
        formData.append("audio", audioBlob, "user_audio.wav");

        let response = await fetch("/transcribe", {
            method: "POST",
            body: formData
        });

        let result = await response.json();
        processUserSpeech(result.transcription);
    };

    mediaRecorder.start();
}

// Stop recording
function stopListening() {
    if (mediaRecorder) {
        mediaRecorder.stop();
    }
}

// Process user speech input
async function processUserSpeech(userSpeech) {
    if (!userSpeech.trim()) return;

    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p><b>You:</b> ${userSpeech}</p>`;

    let response = await fetch("/chat", {
        method: "POST",
        body: JSON.stringify({ message: userSpeech }),
        headers: { "Content-Type": "application/json" }
    });

    let data = await response.json();
    chatBox.innerHTML += `<p><b>AI:</b> ${data.response}</p>`;

    // Convert AI text response to speech using Azure TTS
    if (isAiSpeaking) {
        playAiSpeech(data.response);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

// Toggle AI speech
function toggleAiSpeech() {
    isAiSpeaking = !isAiSpeaking;
    document.getElementById("aiSpeechButton").textContent = isAiSpeaking ? "Mute AI" : "Unmute AI";
}

// AI Text-to-Speech
function speakText(text) {
    let utterance = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utterance);
}

async function playAiSpeech(text) {
    let response = await fetch("/synthesize", {
        method: "POST",
        body: JSON.stringify({ text }),
        headers: { "Content-Type": "application/json" }
    });

    if (!response.ok) {
        console.error("Failed to fetch AI speech");
        return;
    }

    let audioBlob = await response.blob();
    let audioUrl = URL.createObjectURL(audioBlob);

    let audio = new Audio(audioUrl);
    audio.play();
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendTextMessage();
    }
}

async function sendTextMessage() {
    let textInput = document.getElementById("text-input");
    let userSpeech = textInput.value.trim();

    if (userSpeech === "") return;

    textInput.value = ""; // Clear input field
    processUserSpeech(userSpeech);
}