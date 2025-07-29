from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speech_sdk

def main():
    # Get Configuration Settings
    load_dotenv()
    speech_key = os.getenv('SPEECH_KEY')
    speech_region = os.getenv('SPEECH_REGION')

    # Configure translation
    translation_config = speech_sdk.translation.SpeechTranslationConfig(speech_key, speech_region)
    translation_config.speech_recognition_language = 'en-US'
    translation_config.add_target_language('fr')
    translation_config.add_target_language('es')
    translation_config.add_target_language('hi')

    # Configure speech synthesis
    speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)

    print("Speech Translation Service")
    print("=" * 30)
    print("Speak in English and hear translations in French, Spanish, or Hindi")
    print("Say 'quit' to exit\n")

    while True:
        # Get target language
        print("\nSelect target language:")
        print("  fr = French")
        print("  es = Spanish")
        print("  hi = Hindi")
        print("  q = Quit")
        choice = input("Choice: ").lower()
        
        if choice == 'q':
            break
        
        if choice in ['fr', 'es', 'hi']:
            translate_from_microphone(translation_config, speech_config, choice)
        else:
            print("Invalid choice. Please try again.")

def translate_from_microphone(translation_config, speech_config, target_language):
    # Configure microphone input
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config=audio_config)
    
    print(f"\nSpeak now (translating to {target_language})...")
    
    # Get translation
    result = translator.recognize_once_async().get()
    
    if result.reason == speech_sdk.ResultReason.TranslatedSpeech:
        print(f'Recognized: "{result.text}"')
        
        translation = result.translations[target_language]
        print(f"Translation: {translation}")
        
        # Synthesize translation with speaker output
        voices = {
            'fr': 'fr-FR-DeniseNeural',
            'es': 'es-ES-ElviraNeural',
            'hi': 'hi-IN-MadhurNeural'
        }
        
        speech_config.speech_synthesis_voice_name = voices[target_language]
        audio_config = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)
        synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config)
        
        print("Speaking translation...")
        synthesizer.speak_text_async(translation).get()
        
    elif result.reason == speech_sdk.ResultReason.NoMatch:
        print("No speech could be recognized")
    else:
        print(f"Translation failed: {result.reason}")

if __name__ == "__main__":
    main()