import os
import asyncio
from typing import List
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.agents.strategies import SelectionStrategy, TerminationStrategy
from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.chat_history import ChatHistory
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
- Error patterns
- Service failures
- Performance degradation
- Security issues

Always provide a clear assessment of the situation and recommended actions.
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

class ApprovalTerminationStrategy(TerminationStrategy):
    """
    Termination strategy that ends the conversation when both agents agree no action is needed.
    """
    def __init__(self, agents: List[ChatCompletionAgent], max_iterations: int = 10):
        self._agents = agents
        self._max_iterations = max_iterations
        self._iteration_count = 0
        
    async def should_terminate(self, chat_history: ChatHistory) -> bool:
        """Check if the conversation should terminate."""
        self._iteration_count += 1
        
        # Terminate if max iterations reached
        if self._iteration_count >= self._max_iterations:
            return True
            
        # Check if the last message indicates resolution
        if len(chat_history.messages) > 0:
            last_message = chat_history.messages[-1].content.lower()
            
            # Termination phrases
            termination_phrases = [
                "no action needed",
                "incident resolved",
                "all issues resolved",
                "everything is working",
                "no further action required",
                "closing incident"
            ]
            
            for phrase in termination_phrases:
                if phrase in last_message:
                    return True
                    
        return False

class AgentSelectionStrategy(SelectionStrategy):
    """
    Selection strategy that alternates between agents based on the conversation context.
    """
    def __init__(self, agents: List[ChatCompletionAgent]):
        self._agents = {agent.name: agent for agent in agents}
        self._last_speaker = None
        
    async def next_agent(self, chat_history: ChatHistory) -> ChatCompletionAgent:
        """Determine which agent should speak next."""
        # If no messages yet, start with Incident Manager
        if len(chat_history.messages) == 0:
            self._last_speaker = INCIDENT_MANAGER
            return self._agents[INCIDENT_MANAGER]
            
        # Get the last message
        last_message = chat_history.messages[-1]
        last_content = last_message.content.lower()
        
        # Determine next speaker based on content
        if self._last_speaker == INCIDENT_MANAGER:
            # If Incident Manager asked for action, DevOps should respond
            if any(word in last_content for word in ["fix", "restart", "check", "implement", "apply"]):
                self._last_speaker = DEVOPS_ASSISTANT
                return self._agents[DEVOPS_ASSISTANT]
        elif self._last_speaker == DEVOPS_ASSISTANT:
            # After DevOps action, Incident Manager should review
            self._last_speaker = INCIDENT_MANAGER
            return self._agents[INCIDENT_MANAGER]
            
        # Default: alternate speakers
        if self._last_speaker == INCIDENT_MANAGER:
            self._last_speaker = DEVOPS_ASSISTANT
            return self._agents[DEVOPS_ASSISTANT]
        else:
            self._last_speaker = INCIDENT_MANAGER
            return self._agents[INCIDENT_MANAGER]

async def create_agents(kernel: Kernel) -> tuple:
    """Create the Incident Manager and DevOps Assistant agents."""
    # Create Incident Manager agent
    incident_agent = ChatCompletionAgent(
        service_id="incident_manager_service",
        kernel=kernel,
        name=INCIDENT_MANAGER,
        instructions=INCIDENT_MANAGER_INSTRUCTIONS
    )
    
    # Create DevOps Assistant agent
    devops_agent = ChatCompletionAgent(
        service_id="devops_assistant_service",
        kernel=kernel,
        name=DEVOPS_ASSISTANT,
        instructions=DEVOPS_ASSISTANT_INSTRUCTIONS
    )
    
    return incident_agent, devops_agent

async def analyze_logs(log_content: str):
    """Main function to analyze logs using agent orchestration."""
    # Initialize kernels for each agent
    incident_kernel = Kernel()
    devops_kernel = Kernel()
    
    # Configure Azure OpenAI service for each kernel
    azure_chat_service_incident = AzureChatCompletion(
        service_id="incident_manager_service",
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    incident_kernel.add_service(azure_chat_service_incident)
    
    azure_chat_service_devops = AzureChatCompletion(
        service_id="devops_assistant_service",
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    devops_kernel.add_service(azure_chat_service_devops)
    
    # Create agents
    incident_agent, devops_agent = await create_agents(incident_kernel), await create_agents(devops_kernel)
    
    # Actually create the agents properly
    incident_agent = ChatCompletionAgent(
        service_id="incident_manager_service",
        kernel=incident_kernel,
        name=INCIDENT_MANAGER,
        instructions=INCIDENT_MANAGER_INSTRUCTIONS
    )
    
    devops_agent = ChatCompletionAgent(
        service_id="devops_assistant_service",
        kernel=devops_kernel,
        name=DEVOPS_ASSISTANT,
        instructions=DEVOPS_ASSISTANT_INSTRUCTIONS
    )
    
    agents = [incident_agent, devops_agent]
    
    # Create strategies
    termination_strategy = ApprovalTerminationStrategy(agents)
    selection_strategy = AgentSelectionStrategy(agents)
    
    # Create group chat
    chat = AgentGroupChat(
        agents=agents,
        termination_strategy=termination_strategy,
        selection_strategy=selection_strategy
    )
    
    # Start the conversation with the log analysis request
    print("=== AGENT ORCHESTRATION: LOG ANALYSIS ===\n")
    print(f"Analyzing log file...\n")
    
    # Add initial message to trigger analysis
    initial_message = f"Please analyze the following log entries and identify any issues that need attention:\n\n{log_content}"
    
    # Run the group chat
    async for response in chat.invoke(initial_message):
        print(f"[{response.name}]: {response.content}\n")
        print("-" * 80 + "\n")
    
    print("=== ANALYSIS COMPLETE ===")

async def main():
    """Main entry point for the agent orchestration demo."""
    # Sample log content (simulating various scenarios)
    sample_logs = {
        "critical_error": """
[2024-01-20 10:15:23] ERROR: Database connection failed - timeout after 30s
[2024-01-20 10:15:24] ERROR: Failed to connect to primary database
[2024-01-20 10:15:25] WARNING: Failover to secondary database initiated
[2024-01-20 10:15:26] ERROR: Secondary database also unreachable
[2024-01-20 10:15:27] CRITICAL: All database connections lost
[2024-01-20 10:15:28] ERROR: API endpoints returning 500 errors
""",
        "performance_issue": """
[2024-01-20 14:30:15] INFO: API response time: 2500ms
[2024-01-20 14:30:20] WARNING: API response time exceeding threshold: 3200ms
[2024-01-20 14:30:25] WARNING: Memory usage at 87%
[2024-01-20 14:30:30] WARNING: API response time: 4100ms
[2024-01-20 14:30:35] ERROR: Request timeout after 5000ms
[2024-01-20 14:30:40] WARNING: CPU usage at 92%
""",
        "normal_operation": """
[2024-01-20 09:00:00] INFO: System startup completed
[2024-01-20 09:00:15] INFO: All services healthy
[2024-01-20 09:00:30] INFO: API response time: 120ms
[2024-01-20 09:00:45] INFO: Database queries executing normally
[2024-01-20 09:01:00] INFO: Memory usage at 45%
[2024-01-20 09:01:15] INFO: CPU usage at 35%
"""
    }
    
    # Let user choose which scenario to run
    print("Choose a scenario to analyze:")
    print("1. Critical Database Error")
    print("2. Performance Degradation")
    print("3. Normal Operation")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "1":
        await analyze_logs(sample_logs["critical_error"])
    elif choice == "2":
        await analyze_logs(sample_logs["performance_issue"])
    elif choice == "3":
        await analyze_logs(sample_logs["normal_operation"])
    else:
        print("Invalid choice. Running critical error scenario by default.")
        await analyze_logs(sample_logs["critical_error"])

if __name__ == "__main__":
    asyncio.run(main())