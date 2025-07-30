import os
import asyncio
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.functions import KernelArguments
from email_plugin import EmailPlugin

# Load environment variables
load_dotenv()

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

# Define the agent instructions
agent_instructions = """
You are an AI assistant for expense claim submission. Your role is to help employees fill out expense claim forms accurately.

For each expense item, you need to collect:
1. Description of the expense
2. Amount (in USD)
3. Date of expense
4. Category (Travel, Meals, Office Supplies, etc.)

Rules:
- Maximum meal expense is $50 per meal
- Travel expenses require receipts over $25
- Office supplies need manager approval over $100

At the end, summarize all expenses and provide the total amount.
When the user is ready to submit, send an email with all expense details to expense@contoso.com
"""

# Process user interaction using standard chat completion
async def process_expense_claim():
    # Initialize chat history with system message
    chat_history = ChatHistory()
    chat_history.add_system_message(agent_instructions)
    
    print("Expense Assistant: Hello! I'm here to help you submit your expense claim.")
    print("Please describe your expenses one by one, and I'll help you organize them.")
    print("Type 'done' when you've entered all expenses, or 'quit' to exit.\n")
    
    # Track expenses
    expenses = []
    total_amount = 0.0
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            print("Expense Assistant: Goodbye! Your expense claim has been cancelled.")
            break
        
        # Add user message to history
        chat_history.add_user_message(user_input)
        
        # Get response from chat completion
        chat_completion_service = kernel.get_service(service_id)
        response = await chat_completion_service.get_chat_message_content(
            chat_history=chat_history,
            settings=azure_chat_service.get_prompt_execution_settings_class()(
                temperature=0.7,
                max_tokens=500
            )
        )
        
        # Print agent response
        print(f"\nExpense Assistant: {response.content}\n")
        
        # Add assistant response to history
        chat_history.add_assistant_message(response.content)
        
        # Handle 'done' command
        if user_input.lower() == 'done' and len(expenses) > 0:
            print("Expense Assistant: Processing your expense claim...")
            
            # Format and send email using the plugin
            try:
                # Create formatted expense summary
                expense_details = "\n".join([f"- {exp}" for exp in expenses])
                
                # Use the email plugin to format the email
                formatted_body = email_plugin.format_expense_summary(
                    expenses=expense_details,
                    total_amount=total_amount,
                    employee_name="Employee"
                )
                
                # Send the email
                result = email_plugin.send_email(
                    to="expense@contoso.com",
                    subject="Expense Claim Submission",
                    body=formatted_body
                )
                
                print(f"Expense Assistant: {result}")
                print("Your expense claim has been submitted successfully!")
            except Exception as e:
                print(f"Error sending email: {str(e)}")
            break
        
        # Simple expense tracking (in a real scenario, this would be more sophisticated)
        if "expense" in user_input.lower() or "$" in user_input:
            # Try to extract amount
            import re
            amount_match = re.search(r'\$?(\d+(?:\.\d{2})?)', user_input)
            if amount_match:
                amount = float(amount_match.group(1))
                total_amount += amount
                expenses.append(f"{user_input} - ${amount:.2f}")

# Main function
async def main():
    try:
        await process_expense_claim()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())