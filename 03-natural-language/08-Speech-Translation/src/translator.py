from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk


def main():
    try:
        global speech_config
        global translation_config

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


        # Get user input
        targetLanguage = ''
        while targetLanguage != 'quit':
            targetLanguage = input('\nEnter a target language\n fr = French\n es = Spanish\n hi = Hindi\n Enter anything else to stop\n').lower()
            if targetLanguage in translation_config.target_languages:
                Translate(targetLanguage)
            else:
                targetLanguage = 'quit'
                

    except Exception as ex:
        print(ex)

def Translate(targetLanguage):
    translation = ''

    # Translate speech
    current_dir = os.getcwd()
    audio_file = current_dir + '/station.wav'
    audio_config = speech_sdk.AudioConfig(filename=audio_file)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config)
    print("Getting speech from file...")
    result = translator.recognize_once_async().get()
    print('Recognized: "{}"'.format(result.text))
    
    if result.reason == speech_sdk.ResultReason.TranslatedSpeech:
        print("TRANSLATED:")
        for language in result.translations:
            print(f" [{language}] {result.translations[language]}")
            if language == targetLanguage:
                translation = result.translations[language]


    # Synthesize translation
    if translation:
        voices = {
            'fr': 'fr-FR-DeniseNeural',
            'es': 'es-ES-ElviraNeural',
            'hi': 'hi-IN-MadhurNeural'
        }
        speech_config.speech_synthesis_voice_name = voices[targetLanguage]
        
        # Synthesize to file
        output_file = f"translated_{targetLanguage}.wav"
        audio_config = speech_sdk.audio.AudioConfig(filename=output_file)
        speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config)
        speak = speech_synthesizer.speak_text_async(translation).get()
        
        if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
            print(speak.reason)
        else:
            print(f"Translation saved to {output_file}")
            print(f"\n[{targetLanguage}] {translation}")



if __name__ == "__main__":
    main()
