"""
Simple Audio Chat Implementation
Based on Microsoft Learn Lab: Develop an Audio-Enabled Chat App
"""

import os
import base64
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ConnectionType
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Get project endpoint from environment
    project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    if not project_endpoint:
        print("Please set AZURE_AI_PROJECT_ENDPOINT in your .env file")
        return
    
    print("Connecting to Azure AI Foundry project...")
    
    # Create project client
    credential = DefaultAzureCredential()
    project_client = AIProjectClient.from_connection_string(
        conn_str=project_endpoint,
        credential=credential
    )
    
    # Get OpenAI connection
    openai_connection = project_client.connections.get_default(
        connection_type=ConnectionType.AZURE_OPEN_AI
    )
    
    # Create OpenAI client
    openai_client = AzureOpenAI(
        azure_endpoint=openai_connection.endpoint_url,
        api_key=openai_connection.key,
        api_version="2024-08-01-preview"
    )
    
    print("Connected successfully!\n")
    
    # System message for Contoso Produce assistant
    system_message = """You are an AI assistant for Contoso Produce, a supplier of fresh fruits and vegetables. 
    Customers contact you with questions about produce availability, orders, and delivery schedules. 
    You also help with quality concerns and provide information about seasonal products."""
    
    # Interactive chat loop
    print("Contoso Produce AI Assistant")
    print("=" * 40)
    print("Type 'quit' to exit")
    print("Type 'audio <filename>' to include an audio file")
    print("=" * 40)
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("Thank you for using Contoso Produce AI Assistant!")
            break
        
        # Check if user wants to include audio
        if user_input.lower().startswith('audio '):
            # Extract filename
            audio_file = user_input[6:].strip()
            
            # Check if file exists
            if not os.path.exists(audio_file):
                print(f"Error: Audio file '{audio_file}' not found")
                continue
            
            # Get additional text prompt
            text_prompt = input("Additional message (or press Enter): ").strip()
            if not text_prompt:
                text_prompt = "Please analyze this audio and respond appropriately."
            
            # Encode audio file
            try:
                with open(audio_file, 'rb') as f:
                    audio_data = base64.b64encode(f.read()).decode('utf-8')
                
                # Determine audio format
                file_ext = os.path.splitext(audio_file)[1].lower()
                audio_format = file_ext[1:] if file_ext else 'wav'
                
                # Create message with audio
                messages = [
                    {"role": "system", "content": system_message},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": text_prompt},
                            {
                                "type": "input_audio",
                                "input_audio": {
                                    "data": audio_data,
                                    "format": audio_format
                                }
                            }
                        ]
                    }
                ]
                
                print("\nProcessing audio and generating response...")
                
            except Exception as e:
                print(f"Error reading audio file: {e}")
                continue
        
        else:
            # Regular text message
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input}
            ]
        
        # Get response from model
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-audio-preview",  # Use appropriate model
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            
            # Print assistant response
            print(f"\nAssistant: {response.choices[0].message.content}")
            
        except Exception as e:
            print(f"Error getting response: {e}")
            print("Make sure you have deployed the correct model in your Azure AI Foundry project")

if __name__ == "__main__":
    main()