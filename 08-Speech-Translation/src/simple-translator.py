from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speech_sdk

# Get Configuration Settings
load_dotenv()
speech_key = os.getenv('SPEECH_KEY')
speech_region = os.getenv('SPEECH_REGION')

print("Configuring speech translation...")

# Configure translation
translation_config = speech_sdk.translation.SpeechTranslationConfig(speech_key, speech_region)
translation_config.speech_recognition_language = 'en-US'
translation_config.add_target_language('fr')
translation_config.add_target_language('es')
translation_config.add_target_language('hi')

# Configure audio input
audio_config = speech_sdk.AudioConfig(filename="station.wav")

# Create translator
translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config=audio_config)

print("Translating speech from station.wav...")
print("Original language: English (en-US)")
print()

# Get translation
result = translator.recognize_once_async().get()

if result.reason == speech_sdk.ResultReason.TranslatedSpeech:
    print(f'Recognized: "{result.text}"')
    print("\nTranslations:")
    print(f"  French (fr): {result.translations['fr']}")
    print(f"  Spanish (es): {result.translations['es']}")
    print(f"  Hindi (hi): {result.translations['hi']}")
    
    # Now synthesize each translation
    speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
    
    # French
    speech_config.speech_synthesis_voice_name = 'fr-FR-DeniseNeural'
    audio_config = speech_sdk.audio.AudioConfig(filename="translated_fr.wav")
    synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config)
    synthesizer.speak_text_async(result.translations['fr']).get()
    print("\n✓ French audio saved to translated_fr.wav")
    
    # Spanish
    speech_config.speech_synthesis_voice_name = 'es-ES-ElviraNeural'
    audio_config = speech_sdk.audio.AudioConfig(filename="translated_es.wav")
    synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config)
    synthesizer.speak_text_async(result.translations['es']).get()
    print("✓ Spanish audio saved to translated_es.wav")
    
    # Hindi
    speech_config.speech_synthesis_voice_name = 'hi-IN-MadhurNeural'
    audio_config = speech_sdk.audio.AudioConfig(filename="translated_hi.wav")
    synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config)
    synthesizer.speak_text_async(result.translations['hi']).get()
    print("✓ Hindi audio saved to translated_hi.wav")
    
elif result.reason == speech_sdk.ResultReason.NoMatch:
    print("No speech could be recognized")
else:
    print(f"Translation failed: {result.reason}")
    if result.cancellation_details:
        print(f"Error details: {result.cancellation_details.error_details}")