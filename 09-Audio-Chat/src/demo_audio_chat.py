"""
Demo Audio Chat - Simulated responses without Azure connection
This demonstrates the audio chat functionality without requiring Azure setup
"""

import os
import base64
from pathlib import Path
from datetime import datetime

class DemoAudioChatAssistant:
    """Demo version of audio chat assistant with simulated responses."""
    
    def __init__(self):
        self.system_prompt = """You are an AI assistant for Contoso Produce, a fresh produce supplier company. 
        You help customers with product information, orders, delivery schedules, and quality concerns."""
        
        # Simulated responses for demo
        self.demo_responses = {
            "order": "I'd be happy to help you place an order! We have fresh vegetables available including organic lettuce, tomatoes, carrots, and bell peppers. Our minimum order is 10 cases per item. Would you like me to check current pricing and availability for specific items?",
            "quality": "I apologize for any quality issues with your recent delivery. We take product quality very seriously at Contoso Produce. I'll immediately notify our quality assurance team and arrange for a replacement shipment. Can you please provide your order number so I can expedite this for you?",
            "delivery": "Our standard delivery schedule is Monday through Friday, with morning deliveries between 6 AM and 10 AM. For restaurants and priority customers, we offer early morning delivery starting at 4 AM. Same-day delivery is available for orders placed before 2 PM. What delivery timeframe works best for your business?",
            "availability": "For seasonal fruits, we currently have excellent availability of strawberries, blueberries, and peaches. Our organic apple varieties include Gala, Fuji, and Honeycrisp. We also have tropical fruits like mangoes and pineapples arriving fresh twice weekly. What specific fruits are you interested in?",
            "general": "Welcome to Contoso Produce! We're your trusted supplier of fresh fruits and vegetables. We offer both conventional and organic options, competitive wholesale pricing, and reliable delivery service. How can I assist you today?"
        }
    
    def encode_audio_file(self, audio_path: str) -> str:
        """Encode audio file to base64 string."""
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        with open(audio_path, "rb") as audio_file:
            audio_data = audio_file.read()
            encoded_audio = base64.b64encode(audio_data).decode('utf-8')
        
        return encoded_audio
    
    def analyze_audio_context(self, audio_path: str) -> str:
        """Simulate audio analysis by reading accompanying text file."""
        # In demo mode, read the .txt file with same name
        txt_path = audio_path.replace('.wav', '.txt')
        
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as f:
                context = f.read().strip()
        else:
            context = "general inquiry"
        
        # Determine category from context
        if "order" in context.lower():
            return "order"
        elif "quality" in context.lower():
            return "quality"
        elif "delivery" in context.lower():
            return "delivery"
        elif "availability" in context.lower() or "seasonal" in context.lower():
            return "availability"
        else:
            return "general"
    
    def chat_with_audio(self, audio_path: str, text_prompt: str) -> str:
        """Simulate chat with audio input."""
        print(f"[Demo Mode] Processing audio file: {os.path.basename(audio_path)}")
        
        # Encode audio (to demonstrate the process)
        try:
            encoded = self.encode_audio_file(audio_path)
            print(f"[Demo Mode] Audio encoded successfully ({len(encoded)} bytes)")
        except FileNotFoundError:
            return "Error: Audio file not found"
        
        # Analyze context
        category = self.analyze_audio_context(audio_path)
        print(f"[Demo Mode] Detected category: {category}")
        
        # Generate response
        response = self.demo_responses.get(category, self.demo_responses["general"])
        
        if text_prompt and text_prompt != "Please analyze this audio and respond appropriately.":
            response += f"\n\nRegarding your specific question: {text_prompt} - "
            response += "I'll need to check our current inventory and get back to you with detailed information."
        
        return response
    
    def chat_text_only(self, prompt: str) -> str:
        """Simulate text-only chat."""
        prompt_lower = prompt.lower()
        
        # Determine response based on keywords
        if any(word in prompt_lower for word in ["order", "buy", "purchase"]):
            return self.demo_responses["order"]
        elif any(word in prompt_lower for word in ["quality", "bad", "wilted", "rotten"]):
            return self.demo_responses["quality"]
        elif any(word in prompt_lower for word in ["delivery", "deliver", "schedule"]):
            return self.demo_responses["delivery"]
        elif any(word in prompt_lower for word in ["available", "stock", "have", "seasonal"]):
            return self.demo_responses["availability"]
        else:
            return self.demo_responses["general"]

def run_demo():
    """Run the demo audio chat application."""
    print("=" * 60)
    print("CONTOSO PRODUCE - Audio Chat Assistant (Demo Mode)")
    print("=" * 60)
    print("\nThis is a demonstration version that simulates AI responses.")
    print("In production, this would connect to Azure AI Foundry.\n")
    
    assistant = DemoAudioChatAssistant()
    
    # Check if sample audio files exist
    audio_dir = Path("../data/audio_samples")
    if audio_dir.exists():
        audio_files = list(audio_dir.glob("*.wav"))
        if audio_files:
            print("Available sample audio files:")
            for i, audio_file in enumerate(audio_files, 1):
                print(f"{i}. {audio_file.name}")
            print()
    
    print("Commands:")
    print("- Type your message and press Enter")
    print("- Type 'audio <filename>' to include an audio file")
    print("- Type 'demo' to see demo scenarios")
    print("- Type 'quit' to exit")
    print("=" * 60)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("\nThank you for using Contoso Produce AI Assistant!")
            break
        
        elif user_input.lower() == 'demo':
            # Run demo scenarios
            print("\n--- Demo Scenarios ---")
            
            scenarios = [
                ("What organic vegetables do you have?", None),
                ("audio ../data/audio_samples/customer_order.wav", "I need 50 cases by tomorrow"),
                ("audio ../data/audio_samples/quality_concern.wav", "This is the third time this month"),
                ("When can you deliver to downtown restaurants?", None),
                ("audio ../data/audio_samples/product_availability.wav", "Looking for summer fruits")
            ]
            
            for scenario in scenarios:
                if scenario[1]:  # Audio scenario
                    print(f"\nYou: {scenario[0]}")
                    print(f"Additional: {scenario[1]}")
                    
                    audio_file = scenario[0].split()[1]
                    response = assistant.chat_with_audio(audio_file, scenario[1])
                else:  # Text only
                    print(f"\nYou: {scenario[0]}")
                    response = assistant.chat_text_only(scenario[0])
                
                print(f"Assistant: {response}")
            
            print("\n--- End of Demo ---")
        
        elif user_input.lower().startswith('audio '):
            # Process audio file
            audio_file = user_input[6:].strip()
            
            # Get additional prompt
            text_prompt = input("Additional message (or press Enter): ").strip()
            if not text_prompt:
                text_prompt = "Please analyze this audio and respond appropriately."
            
            print(f"\n[Processing audio: {audio_file}]")
            response = assistant.chat_with_audio(audio_file, text_prompt)
            print(f"\nAssistant: {response}")
        
        else:
            # Regular text chat
            response = assistant.chat_text_only(user_input)
            print(f"\nAssistant: {response}")

if __name__ == "__main__":
    run_demo()