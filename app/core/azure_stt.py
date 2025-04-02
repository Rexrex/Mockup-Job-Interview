import os
import azure.cognitiveservices.speech as speechsdk

class Transcriber:
    def __init__(self, key):
        self.azure_key = key  # Needed for session storage
        self.azure_region = "westeurope"
        if not self.azure_key:
            raise ValueError("Missing API key: Set the AZURE_KEY environment variable.")

    def transcribe_audio(self, audio_path):
         speech_key = self.azure_key
         service_region = self.azure_region

         speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
         audio_input = speechsdk.AudioConfig(filename=audio_path)

         recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
         result = recognizer.recognize_once()

         return result.text

    def synthesize_speech_azure(self, text):
        speech_key = self.azure_key
        service_region = self.azure_region

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

        # Save the output instead of playing it
        file_name = "output.wav"
        file_path = os.path.join("audio_files", file_name)

        audio_config = speechsdk.audio.AudioOutputConfig(filename=file_path)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return file_path  # Return the saved file path
        else:
            return None  # Handle errors properly

