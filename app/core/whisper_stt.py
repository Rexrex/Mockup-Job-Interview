import faster_whisper
import os
# Load Faster Whisper model (choose from "small", "medium", "large" models for accuracy/speed)
model = faster_whisper.WhisperModel("base")  # You can use "small", "medium", or "large"


class WhisperTranscriber:
    def __init__(self, model_size="base"):
        """
        Initialize the Faster Whisper model.
        Available models: "tiny", "base", "small", "medium", "large"
        """
        self.model = faster_whisper.WhisperModel(model_size, device="cpu", compute_type="int8")  # Use int8 for speed

    def transcribe_audio(self, audio_path):
        """
        Transcribes the given audio file using Faster Whisper.
        Returns the transcribed text.
        """
        segments, info = self.model.transcribe(audio_path)

        # Combine all segments into one string
        transcription = ' '.join([segment.text for segment in segments])

        return transcription

