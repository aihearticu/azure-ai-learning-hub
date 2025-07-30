# Lab 08: Speech Translation Service

## Overview
This lab demonstrates real-time speech translation using Azure AI Speech Services. The application translates spoken English into French, Spanish, and Hindi, with both text and synthesized speech output.

**Microsoft Learn Module**: [Translate speech](https://microsoftlearning.github.io/mslearn-ai-language/Instructions/Labs/08-translate-speech.html)

## Service Configuration
- **Service Name**: speechservicecuratest
- **Region**: East US
- **Endpoint**: https://eastus.api.cognitive.microsoft.com/

## Learning Objectives
- Configure Azure AI Speech for translation
- Implement multi-language speech translation
- Synthesize translated text to speech
- Work with language-specific neural voices

## Key Features
- **Source Language**: English (en-US)
- **Target Languages**: 
  - French (fr) - Voice: DeniseNeural
  - Spanish (es) - Voice: ElviraNeural  
  - Hindi (hi) - Voice: MadhurNeural
- **Input**: Audio file or microphone
- **Output**: Translated text and synthesized speech

## Project Structure
```
08-Speech-Translation/
├── README.md
├── requirements.txt
├── .env                      # Your credentials (gitignored)
├── .env.example             # Template for credentials
└── src/
    ├── station.wav          # Sample audio: "Where is the station?"
    ├── translator.py        # Original interactive version
    ├── simple-translator.py # Automated translation demo
    ├── translator-mic.py    # Microphone version for Windows
    ├── check-audio.py       # Audio verification tool
    └── translated_*.wav     # Generated translations
```

## Setup Instructions

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/WSL
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Add your Speech service credentials

## Running the Application

### Option 1: File-based Translation (WSL/Linux)
```bash
cd src
python simple-translator.py
```

This will:
- Read "Where is the station?" from `station.wav`
- Translate to French, Spanish, and Hindi
- Generate audio files for each translation

### Option 2: Interactive Mode
```bash
python translator.py
```
Then select target language when prompted.

### Option 3: Microphone Translation (Windows)
```powershell
python translator-mic.py
```
Speak in English and hear real-time translations!

## Translation Examples

**Original**: "Where is the station?"

**Translations**:
- 🇫🇷 **French**: "Où se trouve la gare ?"
- 🇪🇸 **Spanish**: "¿Dónde está la estación?"
- 🇮🇳 **Hindi**: "स्टेशन कहां है?"

## Technical Implementation

### Translation Configuration
```python
translation_config = speech_sdk.translation.SpeechTranslationConfig(speech_key, speech_region)
translation_config.speech_recognition_language = 'en-US'
translation_config.add_target_language('fr')
translation_config.add_target_language('es')
translation_config.add_target_language('hi')
```

### Speech Synthesis
```python
speech_config.speech_synthesis_voice_name = 'fr-FR-DeniseNeural'
synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config)
synthesizer.speak_text_async(translation).get()
```

## Lab Completion
- **Date**: 2025-07-29
- **Status**: ✅ Successfully completed
- **Key Achievement**: Multi-language speech-to-speech translation working perfectly

## Troubleshooting
- For microphone issues in WSL, use Windows PowerShell
- Ensure all language packs are supported in your Speech service region
- Check audio file format (WAV, 16kHz recommended)