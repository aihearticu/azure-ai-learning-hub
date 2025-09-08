# Audio-Enabled Chat Application

This module implements an audio-enabled chat application using Azure AI Foundry and the Phi-4-multimodal-instruct model (or GPT-4 with audio capabilities).

## Overview

This lab demonstrates how to:
- Create an AI assistant for a produce supplier company (Contoso Produce)
- Process both text and audio inputs
- Generate contextual responses based on multimodal inputs
- Handle customer inquiries about products, orders, and deliveries

## Prerequisites

1. **Azure Subscription** with access to Azure AI services
2. **Azure AI Foundry Project** created and configured
3. **Model Deployment**: Deploy Phi-4-multimodal-instruct or gpt-4o-audio-preview
4. **Python 3.8+** installed
5. **Azure CLI** for authentication

## Setup

### 1. Create Azure AI Foundry Project

1. Navigate to [Azure AI Foundry](https://ai.azure.com)
2. Create a new project
3. Deploy the multimodal model (Phi-4-multimodal-instruct or gpt-4o-audio-preview)
4. Note your project endpoint from the project settings

### 2. Configure Environment

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your project endpoint:
   ```
   AZURE_AI_PROJECT_ENDPOINT=your-project-connection-string
   ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Azure Authentication

Sign in to Azure:
```bash
az login
```

## Implementation

### Files Structure

```
09-Audio-Chat/
├── src/
│   ├── audio_chat.py          # Full-featured implementation
│   ├── simple_audio_chat.py   # Simple implementation (lab focus)
│   └── create_sample_audio.py # Generate sample audio files
├── data/
│   └── audio_samples/         # Sample audio files
├── docs/
├── requirements.txt
├── .env.example
└── README.md
```

### Key Components

1. **AudioChatAssistant** (audio_chat.py):
   - Full-featured implementation with multiple capabilities
   - Audio encoding and processing
   - Sentiment analysis
   - Structured responses

2. **Simple Implementation** (simple_audio_chat.py):
   - Focused implementation matching lab requirements
   - Interactive chat loop
   - Audio file support
   - Contoso Produce context

3. **Sample Audio Generator** (create_sample_audio.py):
   - Creates placeholder audio files for testing
   - Simulates different customer scenarios

## Usage

### 1. Generate Sample Audio Files

First, create sample audio files for testing:

```bash
cd src
python create_sample_audio.py
```

This creates sample WAV files in `data/audio_samples/`:
- `customer_order.wav` - Customer placing an order
- `quality_concern.wav` - Quality issue report
- `delivery_inquiry.wav` - Delivery schedule question
- `product_availability.wav` - Product availability check

### 2. Run Simple Audio Chat

Run the simple implementation:

```bash
python simple_audio_chat.py
```

Example interactions:
```
You: What organic vegetables do you have available?
Assistant: We have a great selection of organic vegetables...

You: audio ../data/audio_samples/customer_order.wav
Additional message: Process this order request
Assistant: I'll help you with your order...
```

### 3. Run Full-Featured Chat

For more advanced features:

```bash
python audio_chat.py
```

This includes:
- Audio analysis
- Sentiment detection
- Multiple demo scenarios
- Interactive mode

## Key Features

### 1. Multimodal Input Processing
- Accepts both text and audio inputs
- Encodes audio files to base64
- Supports multiple audio formats (WAV, MP3, M4A)

### 2. Contextual Responses
- AI assistant trained for Contoso Produce context
- Handles product inquiries
- Manages orders and delivery questions
- Addresses quality concerns

### 3. Audio Analysis
- Sentiment analysis from audio
- Urgency detection
- Product mention extraction
- Recommended actions

## Example Scenarios

### Scenario 1: Product Inquiry
```python
User: "What types of apples do you have available?"
Assistant: "We offer several varieties of fresh apples including Gala, Fuji, 
Granny Smith, and Honeycrisp. All are available in both conventional and 
organic options."
```

### Scenario 2: Urgent Order (with audio)
```python
User: audio urgent_order.wav
Context: "Customer needs strawberries for a wedding tomorrow"
Assistant: "I understand this is urgent for your wedding tomorrow. I can arrange 
for 100 cases of fresh strawberries to be delivered first thing in the morning..."
```

### Scenario 3: Quality Concern
```python
User: "The lettuce we received was wilted"
Assistant: "I apologize for the quality issue with your lettuce delivery. 
We take this seriously and I'll arrange for an immediate replacement..."
```

## Technical Details

### Audio Encoding
```python
def encode_audio_file(audio_path: str) -> str:
    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()
        encoded_audio = base64.b64encode(audio_data).decode('utf-8')
    return encoded_audio
```

### Message Format
```python
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": text_prompt},
        {
            "type": "input_audio",
            "input_audio": {
                "data": encoded_audio,
                "format": "wav"
            }
        }
    ]
}
```

### Model Configuration
- Model: `gpt-4o-audio-preview` or `Phi-4-multimodal-instruct`
- Temperature: 0.7 (balanced creativity)
- Max tokens: 300-500 (concise responses)

## Troubleshooting

### Common Issues

1. **Authentication Error**:
   - Ensure you're logged in: `az login`
   - Check your subscription has access to Azure AI services

2. **Model Not Found**:
   - Verify model is deployed in your AI Foundry project
   - Check model name matches your deployment

3. **Audio File Not Found**:
   - Use absolute paths or verify relative paths
   - Ensure audio files exist in specified location

4. **Connection Error**:
   - Verify project endpoint in .env file
   - Check network connectivity
   - Ensure project is in a supported region

### Debug Mode

Set environment variable for detailed logging:
```bash
export AZURE_LOG_LEVEL=DEBUG
```

## Best Practices

1. **Audio Quality**:
   - Use clear audio recordings
   - Minimize background noise
   - Keep audio files reasonably sized

2. **Prompt Engineering**:
   - Provide clear context with audio
   - Be specific about expected responses
   - Use system prompts effectively

3. **Error Handling**:
   - Always validate audio file existence
   - Handle API errors gracefully
   - Provide user-friendly error messages

## Extensions

### Potential Enhancements

1. **Speech Synthesis**:
   - Add text-to-speech for responses
   - Create audio responses

2. **Real-time Audio**:
   - Integrate microphone input
   - Stream audio processing

3. **Advanced Analytics**:
   - Track conversation history
   - Generate insights from interactions
   - Monitor customer satisfaction

4. **Integration**:
   - Connect to order management system
   - Link with inventory database
   - Send notifications

## Resources

- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Audio Processing Best Practices](https://learn.microsoft.com/azure/cognitive-services/speech-service/)

## Summary

This lab demonstrates how to build an audio-enabled chat application that can:
- Process multimodal inputs (text + audio)
- Provide contextual responses for a business scenario
- Handle various customer service situations
- Leverage Azure AI Foundry's advanced models

The implementation serves as a foundation for building sophisticated conversational AI applications that can understand and respond to both text and audio inputs.