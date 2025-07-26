#!/usr/bin/env python3
"""
Azure AI Question Answering Client Application

This application demonstrates how to interact with Azure AI Language's
Question Answering service to create conversational experiences.
"""

import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

# Load environment variables
load_dotenv()


class QuestionAnsweringBot:
    """A simple bot that answers questions using Azure AI Language."""
    
    def __init__(self):
        """Initialize the Question Answering client."""
        # Get configuration from environment
        self.endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        self.key = os.getenv('AI_SERVICE_KEY')
        self.project_name = os.getenv('QA_PROJECT_NAME', 'LearnFAQ')
        self.deployment_name = os.getenv('QA_DEPLOYMENT_NAME', 'production')
        
        # Validate configuration
        if not self.endpoint or not self.key:
            raise ValueError(
                "Please set AI_SERVICE_ENDPOINT and AI_SERVICE_KEY "
                "environment variables"
            )
        
        # Create the client
        self.credential = AzureKeyCredential(self.key)
        self.client = QuestionAnsweringClient(
            endpoint=self.endpoint,
            credential=self.credential
        )
    
    def get_answer(self, question, confidence_threshold=0.3):
        """
        Get an answer for the given question.
        
        Args:
            question: The question to ask
            confidence_threshold: Minimum confidence score (0-1)
            
        Returns:
            tuple: (answer, confidence) or (None, 0) if no answer found
        """
        try:
            # Query the knowledge base
            response = self.client.get_answers(
                question=question,
                project_name=self.project_name,
                deployment_name=self.deployment_name,
                top=3,
                confidence_threshold=confidence_threshold
            )
            
            # Get the best answer
            if response.answers:
                best_answer = response.answers[0]
                return best_answer.answer, best_answer.confidence
            else:
                return None, 0
                
        except Exception as e:
            print(f"Error getting answer: {e}")
            return None, 0
    
    def interactive_session(self):
        """Run an interactive Q&A session."""
        print("Azure AI Question Answering Bot")
        print("=" * 40)
        print("Type 'quit' or 'exit' to end the session")
        print("=" * 40)
        print()
        
        while True:
            # Get user input
            question = input("You: ").strip()
            
            # Check for exit commands
            if question.lower() in ['quit', 'exit', 'bye']:
                print("Bot: Goodbye! Have a great day!")
                break
            
            # Skip empty questions
            if not question:
                continue
            
            # Get answer
            answer, confidence = self.get_answer(question)
            
            # Display response
            if answer:
                print(f"Bot: {answer}")
                print(f"     (Confidence: {confidence:.0%})")
            else:
                print("Bot: I'm sorry, I don't have an answer for that question.")
                print("     Try asking something else!")
            
            print()


def main():
    """Main entry point for the application."""
    try:
        # Create the bot
        bot = QuestionAnsweringBot()
        
        # Run interactive session
        bot.interactive_session()
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease ensure you have:")
        print("1. Created an Azure AI Language resource")
        print("2. Enabled Question Answering feature")
        print("3. Set the required environment variables in .env file")
        
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()