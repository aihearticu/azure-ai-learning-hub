from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speech_sdk

# Get Configuration Settings
load_dotenv()
speech_key = os.getenv('SPEECH_KEY')
speech_region = os.getenv('SPEECH_REGION')

# Configure speech recognition
speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
audio_config = speech_sdk.AudioConfig(filename="station.wav")
speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)

print("Recognizing speech from station.wav...")
result = speech_recognizer.recognize_once_async().get()

if result.reason == speech_sdk.ResultReason.RecognizedSpeech:
    print(f"Recognized: {result.text}")
else:
    print(f"Recognition failed: {result.reason}")