"""
Audio-Enabled Chat Application using Azure AI Foundry
Uses Phi-4-multimodal-instruct model for audio and text understanding
"""

import os
import base64
import json
from typing import Optional, List, Dict
from datetime import datetime
from pathlib import Path
import wave
import numpy as np
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ConnectionType
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AudioChatAssistant:
    """AI Assistant for produce supplier company with audio support."""
    
    def __init__(self):
        """Initialize the audio chat assistant."""
        self.project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        if not self.project_endpoint:
            raise ValueError("Please set AZURE_AI_PROJECT_ENDPOINT in your .env file")
        
        # Initialize Azure AI Project client
        self.credential = DefaultAzureCredential()
        self.project_client = AIProjectClient.from_connection_string(
            conn_str=self.project_endpoint,
            credential=self.credential
        )
        
        # Get OpenAI connection
        self.openai_connection = self.project_client.connections.get_default(
            connection_type=ConnectionType.AZURE_OPEN_AI
        )
        
        # Initialize OpenAI client
        self.openai_client = AzureOpenAI(
            azure_endpoint=self.openai_connection.endpoint_url,
            api_key=self.openai_connection.key,
            api_version="2024-08-01-preview"
        )
        
        # Model configuration
        self.model_name = "gpt-4o-audio-preview"  # or "Phi-4-multimodal-instruct" when available
        self.system_prompt = """You are an AI assistant for Contoso Produce, a fresh produce supplier company. 
        You help customers with product information, orders, delivery schedules, and quality concerns.
        When analyzing audio, pay attention to tone, urgency, and specific product mentions.
        Be helpful, professional, and provide accurate information about produce availability and quality."""
    
    def encode_audio_file(self, audio_path: str) -> str:
        """Encode audio file to base64 string."""
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        with open(audio_path, "rb") as audio_file:
            audio_data = audio_file.read()
            encoded_audio = base64.b64encode(audio_data).decode('utf-8')
        
        return encoded_audio
    
    def create_audio_message(self, audio_path: str, text_prompt: str) -> Dict:
        """Create a message with both audio and text content."""
        encoded_audio = self.encode_audio_file(audio_path)
        
        # Determine audio format from file extension
        file_ext = Path(audio_path).suffix.lower()
        audio_format = {
            '.wav': 'wav',
            '.mp3': 'mp3',
            '.m4a': 'm4a',
            '.ogg': 'ogg'
        }.get(file_ext, 'wav')
        
        message = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": text_prompt
                },
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": encoded_audio,
                        "format": audio_format
                    }
                }
            ]
        }
        
        return message
    
    def chat_with_audio(self, audio_path: str, text_prompt: str) -> str:
        """Send audio and text to the model and get response."""
        try:
            # Create message with audio
            user_message = self.create_audio_message(audio_path, text_prompt)
            
            # Create chat completion
            response = self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    user_message
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error processing audio chat: {str(e)}"
    
    def chat_text_only(self, prompt: str) -> str:
        """Send text-only prompt to the model."""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error processing text chat: {str(e)}"
    
    def analyze_audio_content(self, audio_path: str) -> Dict:
        """Analyze audio content for sentiment, urgency, and key information."""
        analysis_prompt = """Analyze this audio recording and provide:
        1. Overall sentiment (positive/negative/neutral)
        2. Urgency level (high/medium/low)
        3. Main topic or concern
        4. Any specific products mentioned
        5. Recommended action or response"""
        
        try:
            response = self.chat_with_audio(audio_path, analysis_prompt)
            
            # Parse response into structured format
            return {
                "audio_file": os.path.basename(audio_path),
                "analysis": response,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "audio_file": os.path.basename(audio_path),
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

class AudioGenerator:
    """Generate sample audio files for testing."""
    
    @staticmethod
    def create_sample_wav(filename: str, text: str, duration: float = 3.0):
        """Create a simple WAV file with sine wave (placeholder for actual speech)."""
        sample_rate = 44100
        frequency = 440  # A4 note
        
        # Generate time array
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Generate sine wave with varying amplitude (to simulate speech patterns)
        amplitude = np.sin(2 * np.pi * 0.5 * t) * 0.5 + 0.5
        audio_data = amplitude * np.sin(2 * np.pi * frequency * t)
        
        # Add some variations to simulate speech
        for i in range(3):
            freq_variation = 100 + i * 50
            audio_data += 0.2 * np.sin(2 * np.pi * freq_variation * t)
        
        # Normalize
        audio_data = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)
        
        # Write WAV file
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)   # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        # Also save the text content for reference
        with open(filename.replace('.wav', '.txt'), 'w') as txt_file:
            txt_file.write(text)

def demo_basic_chat():
    """Demo basic text chat functionality."""
    print("=== Audio Chat Assistant - Text Chat Demo ===\n")
    
    assistant = AudioChatAssistant()
    
    # Test prompts
    prompts = [
        "What types of apples do you have available?",
        "I need to order 50 cases of tomatoes for next week.",
        "What's the shelf life of your organic lettuce?",
        "Do you offer same-day delivery for restaurants?"
    ]
    
    for prompt in prompts:
        print(f"User: {prompt}")
        response = assistant.chat_text_only(prompt)
        print(f"Assistant: {response}\n")

def demo_audio_chat():
    """Demo audio chat functionality."""
    print("=== Audio Chat Assistant - Audio Chat Demo ===\n")
    
    assistant = AudioChatAssistant()
    audio_gen = AudioGenerator()
    
    # Create sample audio files
    audio_dir = Path("../data/audio_samples")
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate sample audio files (placeholder audio with text descriptions)
    samples = [
        ("order_urgent.wav", "I need 100 cases of strawberries delivered tomorrow morning! This is urgent for a wedding."),
        ("quality_complaint.wav", "The lettuce we received yesterday was wilted. This is unacceptable for our restaurant."),
        ("product_inquiry.wav", "Do you have any organic avocados? What's the price per case?"),
        ("delivery_question.wav", "What time does your delivery truck usually arrive? We need produce before 6 AM.")
    ]
    
    for filename, text in samples:
        audio_path = audio_dir / filename
        audio_gen.create_sample_wav(str(audio_path), text)
        print(f"Created sample audio: {filename}")
    
    print("\nProcessing audio files with chat assistant...\n")
    
    # Process each audio file
    for filename, expected_content in samples:
        audio_path = audio_dir / filename
        
        print(f"Processing: {filename}")
        print(f"Expected content: {expected_content}")
        
        # Analyze audio
        analysis = assistant.analyze_audio_content(str(audio_path))
        print(f"Analysis: {json.dumps(analysis, indent=2)}")
        
        # Get response with context
        prompt = f"Respond to this customer inquiry from the audio. Context: {expected_content}"
        response = assistant.chat_with_audio(str(audio_path), prompt)
        print(f"Response: {response}\n")

def demo_multimodal_scenarios():
    """Demo various multimodal scenarios."""
    print("=== Audio Chat Assistant - Multimodal Scenarios ===\n")
    
    assistant = AudioChatAssistant()
    
    scenarios = [
        {
            "name": "Order Modification",
            "audio_context": "Customer sounds stressed about changing their order",
            "text": "The customer in the audio wants to modify their order. What should we do?"
        },
        {
            "name": "Quality Assurance",
            "audio_context": "Customer reporting quality issues with delivered produce",
            "text": "Based on the audio complaint, what quality control measures should we implement?"
        },
        {
            "name": "Urgent Delivery",
            "audio_context": "Restaurant owner needs emergency produce delivery",
            "text": "The audio contains an urgent delivery request. How can we accommodate this?"
        }
    ]
    
    for scenario in scenarios:
        print(f"Scenario: {scenario['name']}")
        print(f"Context: {scenario['audio_context']}")
        
        # Simulate with text (since we're using placeholder audio)
        full_prompt = f"{scenario['text']}\n\nAudio context: {scenario['audio_context']}"
        response = assistant.chat_text_only(full_prompt)
        print(f"Assistant Response: {response}\n")

def interactive_chat():
    """Run interactive chat session."""
    print("=== Audio Chat Assistant - Interactive Mode ===")
    print("Type 'quit' to exit, 'audio <filename>' to process audio file\n")
    
    assistant = AudioChatAssistant()
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        elif user_input.lower().startswith('audio '):
            # Process audio file
            audio_file = user_input[6:].strip()
            if os.path.exists(audio_file):
                prompt = input("Additional context or question: ")
                response = assistant.chat_with_audio(audio_file, prompt)
                print(f"Assistant: {response}\n")
            else:
                print(f"Audio file not found: {audio_file}\n")
        
        else:
            # Regular text chat
            response = assistant.chat_text_only(user_input)
            print(f"Assistant: {response}\n")

if __name__ == "__main__":
    print("Azure AI Audio Chat Assistant for Contoso Produce\n")
    
    # Check for environment configuration
    if not os.getenv("AZURE_AI_PROJECT_ENDPOINT"):
        print("Please configure your .env file with AZURE_AI_PROJECT_ENDPOINT")
        print("You can get this from your Azure AI Foundry project settings")
        exit(1)
    
    # Run demos
    try:
        # Text chat demo
        demo_basic_chat()
        
        # Audio chat demo (with generated samples)
        # Note: This creates placeholder audio files since we can't generate real speech
        demo_audio_chat()
        
        # Multimodal scenarios
        demo_multimodal_scenarios()
        
        # Interactive mode
        print("\nStarting interactive mode...")
        interactive_chat()
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. Created an Azure AI Foundry project")
        print("2. Deployed the required model")
        print("3. Configured your .env file correctly")