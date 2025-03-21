import os

import azure.cognitiveservices.speech as speechsdk

class Transcriber:
    def __init__(self):
        self.azure_key = os.environ.get('AZURE_KEY')
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
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        synthesizer.speak_text_async(text)

