#!/usr/bin/env python3
"""Demo script for the expense agent with pre-defined inputs"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from email_plugin import EmailPlugin

# Load environment variables
load_dotenv()

async def demo_expense_claim():
    """Run a demo of the expense agent with pre-defined inputs"""
    
    # Initialize kernel
    kernel = Kernel()
    
    # Configure Azure OpenAI service
    service_id = "azure_openai"
    azure_chat_service = AzureChatCompletion(
        service_id=service_id,
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    kernel.add_service(azure_chat_service)
    
    # Add Email Plugin
    email_plugin = EmailPlugin()
    kernel.add_plugin(email_plugin, "EmailPlugin")
    
    # Define agent instructions
    agent_instructions = """
    You are an AI assistant for expense claim submission. Help employees fill out expense claims.
    Validate expenses according to company rules: max $50 for meals, receipts required for travel over $25.
    """
    
    # Initialize chat history
    chat_history = ChatHistory()
    chat_history.add_system_message(agent_instructions)
    
    print("=== EXPENSE AGENT DEMO ===\n")
    print("This is a demonstration of the expense agent with pre-defined inputs.\n")
    
    # Simulate user inputs
    demo_inputs = [
        "I had lunch with a client yesterday for $45",
        "I bought office supplies for $23.50",
        "I took a taxi to the airport for $35"
    ]
    
    expenses = []
    total = 0.0
    
    # Process each input
    for user_input in demo_inputs:
        print(f"User: {user_input}")
        chat_history.add_user_message(user_input)
        
        # Get AI response
        chat_completion_service = kernel.get_service(service_id)
        response = await chat_completion_service.get_chat_message_content(
            chat_history=chat_history,
            settings=azure_chat_service.get_prompt_execution_settings_class()(
                temperature=0.7,
                max_tokens=300
            )
        )
        
        print(f"Agent: {response.content}\n")
        chat_history.add_assistant_message(response.content)
        
        # Track expenses
        if "$" in user_input:
            import re
            amount_match = re.search(r'\$?(\d+(?:\.\d{2})?)', user_input)
            if amount_match:
                amount = float(amount_match.group(1))
                total += amount
                expenses.append(f"{user_input}")
    
    # Submit the claim
    print("User: I'm done with my expenses, please submit them")
    print("\nAgent: Processing your expense claim...\n")
    
    # Format and send email
    expense_details = "\n".join([f"- {exp}" for exp in expenses])
    
    formatted_body = email_plugin.format_expense_summary(
        expenses=expense_details,
        total_amount=total,
        employee_name="Demo Employee"
    )
    
    result = email_plugin.send_email(
        to="expense@contoso.com",
        subject="Expense Claim Submission - Demo",
        body=formatted_body
    )
    
    print(f"Agent: {result}")
    print("Your expense claim has been submitted successfully!")
    print(f"\\nTotal expenses: ${total:.2f}")

if __name__ == "__main__":
    asyncio.run(demo_expense_claim())