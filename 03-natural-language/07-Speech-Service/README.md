# Lab 07: Azure AI Speech Service - Speaking Clock Application

## Overview
This lab demonstrates how to create a speech-enabled application using Azure AI Speech Services for both speech recognition (speech-to-text) and speech synthesis (text-to-speech).

**Microsoft Learn Module**: [Create a speech-enabled app](https://microsoftlearning.github.io/mslearn-ai-language/Instructions/Labs/07-speech.html)

## Service Configuration
- **Service Name**: speechservicecuratest
- **Region**: East US
- **Endpoint**: https://eastus.api.cognitive.microsoft.com/

## Learning Objectives
- Configure Azure AI Speech service
- Implement speech-to-text recognition
- Implement text-to-speech synthesis
- Build a speaking clock application
- Work with SSML for advanced speech synthesis

## Prerequisites
- Azure subscription
- Python 3.8+
- Azure Speech SDK

## Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Add your Speech service credentials

3. **Run the application**:
   ```bash
   python src/speaking-clock.py
   ```

## Project Structure
```
07-Speech-Service/
├── README.md
├── .env                    # Your credentials (gitignored)
├── .env.example           # Template for credentials
├── requirements.txt       # Python dependencies
├── src/
│   ├── speaking-clock.py  # Main application
│   └── time.wav          # Sample audio file
└── output/               # Generated audio files
```

## Key Features Implemented
- [x] Speech recognition from audio file
- [x] Speech recognition from microphone
- [x] Text-to-speech synthesis
- [x] Voice selection (en-GB-RyanNeural, en-GB-LibbyNeural)
- [x] SSML support for advanced speech control

## Files Created
- `speaking-clock.py` - Main application using audio files
- `speaking-clock-mic.py` - Version with microphone/speaker support
- `time.wav` - Sample audio input ("What time is it?")
- `output.wav` - Generated speech output

## Key Code Components

### Speech Recognition
```python
audio_config = speech_sdk.AudioConfig(filename=audioFile)
speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
speech = speech_recognizer.recognize_once_async().get()
```

### Speech Synthesis with SSML
```python
responseSsml = """
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
        <voice name='en-GB-LibbyNeural'>
            {}
            <break strength='weak'/>
            Time to end this lab!
        </voice>
    </speak>
""".format(response_text)
speak = speech_synthesizer.speak_ssml_async(responseSsml).get()
```

## Running with Microphone Support

### Option 1: WSL with Audio Files (Default)
```bash
cd src
source ../venv/bin/activate
python speaking-clock.py
```

### Option 2: Windows with Microphone
For real microphone/speaker support, run from Windows PowerShell:

1. **Navigate to WSL files from Windows**:
   ```powershell
   cd \\wsl.localhost\Ubuntu\home\jjhpe
   cd "Azure AI Engineer\Azure AI Services Container\Azure-AI-Learning-Modules\07-Speech-Service\src"
   ```

2. **Copy environment file**:
   ```powershell
   copy ..\.env .
   ```

3. **Install dependencies**:
   ```powershell
   pip install python-dotenv azure-cognitiveservices-speech
   ```

4. **Run microphone version**:
   ```powershell
   python speaking-clock-mic.py
   ```

## Common Issues and Solutions

### WSL Microphone Error
- **Error**: `SPXERR_MIC_NOT_AVAILABLE`
- **Solution**: WSL doesn't have direct microphone access. Use Windows PowerShell instead.

### Path Navigation in Windows
- Use PowerShell instead of CMD for UNC path support
- Navigate step by step if long paths cause issues

## Lab Completion
- **Date**: 2025-07-29
- **Status**: ✅ Successfully completed
- **Key Achievement**: Full speech recognition and synthesis working with live microphone on Windows

## Security Note
Never commit your `.env` file with actual credentials to version control.