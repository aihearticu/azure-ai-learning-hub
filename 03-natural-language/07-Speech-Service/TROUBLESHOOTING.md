# Speech Service Troubleshooting Guide

## Common Issues and Solutions

### 1. Microphone Not Available in WSL
**Error**: `Exception with an error code: 0xe (SPXERR_MIC_NOT_AVAILABLE)`

**Cause**: WSL (Windows Subsystem for Linux) doesn't have direct access to Windows audio hardware.

**Solutions**:
- **Recommended**: Run the script from Windows PowerShell instead
- Use the file-based version (`speaking-clock.py`) in WSL
- Advanced: Set up PulseAudio server on Windows (complex)

### 2. Path Navigation Issues in Windows
**Error**: `CMD does not support UNC paths as current directories`

**Cause**: Windows Command Prompt doesn't support `\\wsl$` paths directly.

**Solution**: Use PowerShell instead of CMD:
```powershell
cd \\wsl.localhost\Ubuntu\home\username
```

### 3. Azure Authentication Errors
**Error**: `AuthorizationFailed` or incorrect region

**Solutions**:
- Verify your Speech service key in `.env` file
- Ensure region matches your Azure resource (e.g., `eastus`)
- Check for typos in credentials
- Regenerate keys in Azure Portal if needed

### 4. Module Import Errors
**Error**: `ModuleNotFoundError: No module named 'azure.cognitiveservices.speech'`

**Solution**:
```bash
pip install azure-cognitiveservices-speech
```

### 5. Audio File Not Found
**Error**: `FileNotFoundError` for `time.wav`

**Solution**: Ensure you're running from the `src` directory where the audio files are located.

### 6. Virtual Environment Issues
**Error**: `error: externally-managed-environment`

**Solution**: Create and use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/WSL
# or
venv\Scripts\activate  # Windows
```

### 7. Speech Recognition Returns Empty
**Possible Causes**:
- Microphone not properly configured
- Background noise interference
- Speaking too quickly or quietly

**Solutions**:
- Check Windows sound settings
- Use a headset for better audio quality
- Speak clearly after the "Speak now..." prompt

### 8. Text-to-Speech No Audio Output
**Possible Causes**:
- Speaker/audio output not configured
- File saved but not played

**Solutions**:
- Check the `output.wav` file was created
- Ensure speakers are connected and volume is up
- Try the speaker version (`speaking-clock-mic.py`) on Windows

## Platform-Specific Notes

### WSL Users
- Audio hardware access is limited
- Use file-based I/O for testing
- Run on native Windows for full microphone support

### Windows Users
- Use PowerShell for WSL file access
- Install Python from python.org or Microsoft Store
- Ensure microphone permissions are granted

### Linux/Mac Users
- May need to install additional audio libraries
- Check microphone permissions in system settings

## Quick Diagnostic Commands

Check Python version:
```bash
python --version
```

Check installed packages:
```bash
pip list | grep azure
```

Test microphone (Linux):
```bash
arecord -l
```

Test Azure connection:
```python
import azure.cognitiveservices.speech as speech_sdk
config = speech_sdk.SpeechConfig("your-key", "your-region")
print(f"Connected to region: {config.region}")
```