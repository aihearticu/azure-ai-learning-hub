import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
import user_functions
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

class TechnicalSupportAgent:
    """AI Agent for technical support with custom function integration."""
    
    def __init__(self):
        """Initialize the support agent."""
        self.client = AzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version="2024-02-15-preview"
        )
        self.deployment_name = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
        
        # Define available functions
        self.functions = [
            {
                "type": "function",
                "function": {
                    "name": "submit_support_ticket",
                    "description": "Submit a technical support ticket for the customer",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "email_address": {
                                "type": "string",
                                "description": "Customer's email address"
                            },
                            "description": {
                                "type": "string",
                                "description": "Detailed description of the technical issue"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high", "critical"],
                                "description": "Priority level of the ticket"
                            }
                        },
                        "required": ["email_address", "description"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_ticket_status",
                    "description": "Check the status of an existing support ticket",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ticket_number": {
                                "type": "string",
                                "description": "The ticket number to check"
                            }
                        },
                        "required": ["ticket_number"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "escalate_ticket",
                    "description": "Escalate a support ticket to higher priority",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ticket_number": {
                                "type": "string",
                                "description": "The ticket number to escalate"
                            },
                            "reason": {
                                "type": "string",
                                "description": "Reason for escalation"
                            }
                        },
                        "required": ["ticket_number", "reason"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_knowledge_base_article",
                    "description": "Search for knowledge base articles on a specific topic",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "The topic to search for (e.g., password_reset, vpn_setup, printer_issues)"
                            }
                        },
                        "required": ["topic"]
                    }
                }
            }
        ]
        
        # System prompt
        self.system_prompt = """You are a helpful technical support agent. Your role is to:
        1. Assist customers with technical issues
        2. Collect necessary information about their problems
        3. Search the knowledge base for solutions
        4. Submit support tickets when needed
        5. Check ticket status and escalate when appropriate
        
        Always be professional, empathetic, and thorough. Ask clarifying questions when needed.
        Try to resolve issues using knowledge base articles first before creating tickets.
        When creating tickets, ensure you have the customer's email and a detailed problem description."""
        
        # Initialize conversation history
        self.messages = [{"role": "system", "content": self.system_prompt}]
    
    def process_message(self, user_message: str) -> str:
        """Process a user message and return the agent's response."""
        # Add user message to history
        self.messages.append({"role": "user", "content": user_message})
        
        # Get response from OpenAI
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=self.messages,
            tools=self.functions,
            tool_choice="auto",
            temperature=0.7,
            max_tokens=500
        )
        
        # Process the response
        assistant_message = response.choices[0].message
        
        # Check if the assistant wants to use a function
        if assistant_message.tool_calls:
            # Add assistant's message to history
            self.messages.append(assistant_message)
            
            # Process function calls
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Call the appropriate function
                if function_name == "submit_support_ticket":
                    result = user_functions.submit_support_ticket(**function_args)
                elif function_name == "check_ticket_status":
                    result = user_functions.check_ticket_status(**function_args)
                elif function_name == "escalate_ticket":
                    result = user_functions.escalate_ticket(**function_args)
                elif function_name == "get_knowledge_base_article":
                    result = user_functions.get_knowledge_base_article(**function_args)
                else:
                    result = json.dumps({"error": f"Unknown function: {function_name}"})
                
                # Add function result to messages
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # Get final response after function execution
            final_response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=self.messages,
                temperature=0.7,
                max_tokens=500
            )
            
            final_message = final_response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": final_message})
            
            return final_message
        else:
            # No function call, just return the response
            self.messages.append({"role": "assistant", "content": assistant_message.content})
            return assistant_message.content
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.messages = [{"role": "system", "content": self.system_prompt}]

def main():
    """Main function to demonstrate the support agent."""
    print("=== Technical Support Agent ===")
    print("Type 'quit' to exit, 'reset' to start a new conversation\n")
    
    agent = TechnicalSupportAgent()
    
    # Initial greeting
    print("Support Agent: Hello! I'm your technical support assistant. How can I help you today?")
    print("I can help you with:")
    print("- Searching our knowledge base for solutions")
    print("- Submitting support tickets")
    print("- Checking ticket status")
    print("- Escalating urgent issues\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("Support Agent: Thank you for contacting support. Have a great day!")
            break
        elif user_input.lower() == 'reset':
            agent.reset_conversation()
            print("Support Agent: Conversation reset. How can I help you?")
            continue
        
        # Process message
        response = agent.process_message(user_input)
        print(f"\nSupport Agent: {response}\n")

def demo_mode():
    """Run a demonstration of the support agent capabilities."""
    print("=== Technical Support Agent Demo ===\n")
    
    agent = TechnicalSupportAgent()
    
    # Demo scenarios
    scenarios = [
        "I can't connect to the VPN. Can you help?",
        "I need to reset my password but don't know how.",
        "My email isn't working. This is urgent! My email is john.doe@company.com",
        "Can you check the status of ticket ABC12345?",
        "I submitted a ticket yesterday but haven't heard back. Can you escalate it? The ticket number is ABC12345 and it's affecting my entire team."
    ]
    
    for scenario in scenarios:
        print(f"Customer: {scenario}")
        response = agent.process_message(scenario)
        print(f"Support Agent: {response}\n")
        print("-" * 80 + "\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_mode()
    else:
        main()