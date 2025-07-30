import os
import asyncio
from typing import List, Dict
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

# Load environment variables
load_dotenv()

# Agent names
INCIDENT_MANAGER = "IncidentManager"
DEVOPS_ASSISTANT = "DevOpsAssistant"

# Agent instructions
INCIDENT_MANAGER_INSTRUCTIONS = """
You are an Incident Manager responsible for monitoring and managing service incidents.
Your responsibilities include:
1. Analyzing log files to identify issues
2. Determining the severity of incidents
3. Coordinating with DevOps to resolve issues
4. Providing clear status updates
5. Deciding when incidents are resolved

When analyzing logs, look for:
- ERROR and CRITICAL log entries
- Service failures and timeouts
- Performance degradation (high response times, high CPU/memory)
- Security issues

Always provide a clear assessment and recommended actions.
"""

DEVOPS_ASSISTANT_INSTRUCTIONS = """
You are a DevOps Assistant responsible for technical implementation and fixes.
Your responsibilities include:
1. Implementing technical solutions
2. Restarting services when needed
3. Checking system health
4. Applying patches or configuration changes
5. Providing technical analysis

When given a task:
- Explain what actions you're taking
- Provide technical details
- Confirm when tasks are completed
- Report any complications
"""

class MultiAgentOrchestrator:
    """Orchestrates conversation between multiple agents."""
    
    def __init__(self):
        self.agents = {}
        self.chat_histories = {}
        self.kernels = {}
        
    def add_agent(self, name: str, instructions: str, kernel: Kernel):
        """Add an agent to the orchestrator."""
        self.agents[name] = instructions
        self.kernels[name] = kernel
        self.chat_histories[name] = ChatHistory()
        self.chat_histories[name].add_system_message(instructions)
        
    async def get_agent_response(self, agent_name: str, message: str) -> str:
        """Get response from a specific agent."""
        # Add the message to the agent's chat history
        self.chat_histories[agent_name].add_user_message(message)
        
        # Get the kernel and service for this agent
        kernel = self.kernels[agent_name]
        service_id = f"{agent_name.lower()}_service"
        chat_service = kernel.get_service(service_id)
        
        # Get response
        response = await chat_service.get_chat_message_content(
            chat_history=self.chat_histories[agent_name],
            settings=chat_service.get_prompt_execution_settings_class()(
                temperature=0.7,
                max_tokens=500
            )
        )
        
        # Add response to history
        self.chat_histories[agent_name].add_assistant_message(response.content)
        
        return response.content
    
    async def orchestrate_conversation(self, initial_message: str, max_turns: int = 10):
        """Orchestrate a conversation between agents."""
        print("=== MULTI-AGENT ORCHESTRATION ===\n")
        
        current_message = initial_message
        current_agent = INCIDENT_MANAGER  # Start with Incident Manager
        
        for turn in range(max_turns):
            # Get response from current agent
            print(f"[{current_agent}]:")
            response = await self.get_agent_response(current_agent, current_message)
            print(f"{response}\n")
            print("-" * 80 + "\n")
            
            # Check for termination conditions
            if any(phrase in response.lower() for phrase in [
                "no action needed", "incident resolved", "all issues resolved",
                "everything is working", "no further action required"
            ]):
                print("=== CONVERSATION COMPLETE - Issue Resolved ===")
                break
            
            # Prepare message for next agent
            current_message = f"Based on the analysis: {response}"
            
            # Switch agents
            if current_agent == INCIDENT_MANAGER:
                # Check if action is needed
                if any(word in response.lower() for word in [
                    "restart", "fix", "implement", "check", "investigate", "apply"
                ]):
                    current_agent = DEVOPS_ASSISTANT
                else:
                    # No action needed, end conversation
                    print("=== CONVERSATION COMPLETE - No Action Required ===")
                    break
            else:
                # After DevOps action, go back to Incident Manager
                current_agent = INCIDENT_MANAGER
                current_message = f"DevOps has completed the following actions: {response}\nPlease verify if the issue is resolved."
        
        if turn == max_turns - 1:
            print("=== CONVERSATION COMPLETE - Max Turns Reached ===")

async def main():
    """Main entry point for the multi-agent demo."""
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator()
    
    # Create kernel for Incident Manager
    incident_kernel = Kernel()
    incident_service = AzureChatCompletion(
        service_id=f"{INCIDENT_MANAGER.lower()}_service",
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    incident_kernel.add_service(incident_service)
    
    # Create kernel for DevOps Assistant
    devops_kernel = Kernel()
    devops_service = AzureChatCompletion(
        service_id=f"{DEVOPS_ASSISTANT.lower()}_service",
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    devops_kernel.add_service(devops_service)
    
    # Add agents to orchestrator
    orchestrator.add_agent(INCIDENT_MANAGER, INCIDENT_MANAGER_INSTRUCTIONS, incident_kernel)
    orchestrator.add_agent(DEVOPS_ASSISTANT, DEVOPS_ASSISTANT_INSTRUCTIONS, devops_kernel)
    
    # Sample scenarios
    scenarios = {
        "1": {
            "name": "Critical Database Error",
            "logs": """[2024-01-20 10:15:23] ERROR: Database connection failed - timeout after 30s
[2024-01-20 10:15:24] ERROR: Failed to connect to primary database
[2024-01-20 10:15:25] WARNING: Failover to secondary database initiated
[2024-01-20 10:15:26] ERROR: Secondary database also unreachable
[2024-01-20 10:15:27] CRITICAL: All database connections lost
[2024-01-20 10:15:28] ERROR: API endpoints returning 500 errors"""
        },
        "2": {
            "name": "Performance Degradation",
            "logs": """[2024-01-20 14:30:15] INFO: API response time: 2500ms
[2024-01-20 14:30:20] WARNING: API response time exceeding threshold: 3200ms
[2024-01-20 14:30:25] WARNING: Memory usage at 87%
[2024-01-20 14:30:30] WARNING: API response time: 4100ms
[2024-01-20 14:30:35] ERROR: Request timeout after 5000ms
[2024-01-20 14:30:40] WARNING: CPU usage at 92%"""
        },
        "3": {
            "name": "Normal Operation",
            "logs": """[2024-01-20 09:00:00] INFO: System startup completed
[2024-01-20 09:00:15] INFO: All services healthy
[2024-01-20 09:00:30] INFO: API response time: 120ms
[2024-01-20 09:00:45] INFO: Database queries executing normally
[2024-01-20 09:01:00] INFO: Memory usage at 45%
[2024-01-20 09:01:15] INFO: CPU usage at 35%"""
        }
    }
    
    # Display menu
    print("Multi-Agent Orchestration Demo")
    print("=" * 40)
    print("\nChoose a scenario to analyze:")
    for key, scenario in scenarios.items():
        print(f"{key}. {scenario['name']}")
    print("4. Load custom log file")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice in scenarios:
        scenario = scenarios[choice]
        print(f"\n=== Analyzing: {scenario['name']} ===\n")
        initial_message = f"Please analyze these log entries and determine if any action is needed:\n\n{scenario['logs']}"
        await orchestrator.orchestrate_conversation(initial_message)
    elif choice == "4":
        # Load custom log file
        log_files = os.listdir("../data")
        print("\nAvailable log files:")
        for i, file in enumerate(log_files):
            if file.endswith('.log'):
                print(f"{i+1}. {file}")
        
        file_choice = input("\nSelect a log file number: ").strip()
        try:
            file_index = int(file_choice) - 1
            log_file = log_files[file_index]
            with open(f"../data/{log_file}", 'r') as f:
                log_content = f.read()
            
            print(f"\n=== Analyzing: {log_file} ===\n")
            initial_message = f"Please analyze these log entries and determine if any action is needed:\n\n{log_content}"
            await orchestrator.orchestrate_conversation(initial_message)
        except (ValueError, IndexError, FileNotFoundError):
            print("Invalid selection. Using default scenario.")
            await orchestrator.orchestrate_conversation(
                f"Please analyze these log entries:\n\n{scenarios['1']['logs']}"
            )
    else:
        print("Invalid choice. Running critical error scenario.")
        await orchestrator.orchestrate_conversation(
            f"Please analyze these log entries:\n\n{scenarios['1']['logs']}"
        )

if __name__ == "__main__":
    asyncio.run(main())