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
    print('Ready to translate from', translation_config.speech_recognition_language)

    # Configure speech
    speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)

    # Test all languages
    for target_language in ['fr', 'es', 'hi']:
        print(f"\n--- Translating to {target_language} ---")
        translate_speech(translation_config, speech_config, target_language)

def translate_speech(translation_config, speech_config, target_language):
    # Translate speech from file
    current_dir = os.getcwd()
    audio_file = current_dir + '/station.wav'
    audio_config = speech_sdk.AudioConfig(filename=audio_file)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config)
    
    print("Getting speech from file...")
    result = translator.recognize_once_async().get()
    print('Recognized: "{}"'.format(result.text))
    
    if result.reason == speech_sdk.ResultReason.TranslatedSpeech:
        translation = result.translations[target_language]
        print(f"Translated to {target_language}: {translation}")
        
        # Synthesize translation
        voices = {
            'fr': 'fr-FR-DeniseNeural',
            'es': 'es-ES-ElviraNeural',
            'hi': 'hi-IN-MadhurNeural'
        }
        speech_config.speech_synthesis_voice_name = voices[target_language]
        
        # Synthesize to file
        output_file = f"translated_{target_language}.wav"
        audio_config = speech_sdk.audio.AudioConfig(filename=output_file)
        speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config)
        speak = speech_synthesizer.speak_text_async(translation).get()
        
        if speak.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
            print(f"✓ Translation audio saved to {output_file}")

if __name__ == "__main__":
    main()