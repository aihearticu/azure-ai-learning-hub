import os
import asyncio
from typing import Optional
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentCreationRequest, AgentToolDefinition, CodeInterpreterToolDefinition
from azure.ai.projects.models import ThreadCreationRequest, MessageCreationRequest, RunCreationRequest
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv()

class DataAnalysisAgent:
    """AI Agent for data analysis using Code Interpreter."""
    
    def __init__(self):
        """Initialize the agent client."""
        self.endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
        self.api_key = os.environ["AZURE_OPENAI_API_KEY"]
        self.deployment_name = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
        
        # Create AI Project client with key authentication
        self.client = AIProjectClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key)
        )
        
        self.agent = None
        self.thread = None
        
    async def create_agent(self):
        """Create an AI agent with Code Interpreter tool."""
        print("Creating AI Agent with Code Interpreter...")
        
        # Define Code Interpreter tool
        code_interpreter = CodeInterpreterToolDefinition()
        
        # Create agent request
        agent_request = AgentCreationRequest(
            model=self.deployment_name,
            name="data-analyst",
            instructions="""You are a data analyst AI agent. Your role is to:
            1. Analyze data files provided by users
            2. Generate insights and visualizations
            3. Create charts and graphs using Python
            4. Provide clear explanations of findings
            
            When analyzing data:
            - First explore the data structure
            - Identify key patterns and trends
            - Create appropriate visualizations
            - Summarize findings clearly""",
            tools=[code_interpreter]
        )
        
        # Create the agent
        self.agent = await self.client.agents.create_agent(agent_request)
        print(f"Agent created: {self.agent.id}")
        return self.agent
    
    async def upload_file(self, file_path: str):
        """Upload a file for the agent to analyze."""
        print(f"Uploading file: {file_path}")
        
        with open(file_path, 'rb') as file:
            uploaded_file = await self.client.files.upload(
                file=file,
                purpose="assistants"
            )
        
        print(f"File uploaded: {uploaded_file.id}")
        return uploaded_file
    
    async def create_thread_with_file(self, file_id: str):
        """Create a thread with an attached file."""
        print("Creating thread...")
        
        thread_request = ThreadCreationRequest(
            messages=[
                MessageCreationRequest(
                    role="user",
                    content="I've uploaded a data file. Please analyze it and provide insights.",
                    file_ids=[file_id]
                )
            ]
        )
        
        self.thread = await self.client.agents.create_thread(thread_request)
        print(f"Thread created: {self.thread.id}")
        return self.thread
    
    async def analyze_data(self, user_prompt: str):
        """Send analysis request to the agent."""
        print(f"\nUser: {user_prompt}")
        
        # Add user message to thread
        await self.client.agents.create_message(
            thread_id=self.thread.id,
            message=MessageCreationRequest(
                role="user",
                content=user_prompt
            )
        )
        
        # Create and process run
        run_request = RunCreationRequest(
            assistant_id=self.agent.id
        )
        
        run = await self.client.agents.create_run(
            thread_id=self.thread.id,
            run=run_request
        )
        
        # Wait for run completion
        print("Processing...")
        while run.status in ["queued", "in_progress", "requires_action"]:
            await asyncio.sleep(2)
            run = await self.client.agents.get_run(
                thread_id=self.thread.id,
                run_id=run.id
            )
            
            if run.status == "requires_action":
                # Handle any required actions
                print("Action required by agent...")
        
        if run.status == "completed":
            # Get messages
            messages = await self.client.agents.list_messages(
                thread_id=self.thread.id
            )
            
            # Display assistant's response
            for message in messages.data:
                if message.role == "assistant" and message.created_at > run.created_at:
                    print(f"\nAssistant: {message.content[0].text.value}")
                    
                    # Check for any generated files (charts, etc.)
                    if hasattr(message.content[0], 'file_ids') and message.content[0].file_ids:
                        print("Generated files:", message.content[0].file_ids)
        else:
            print(f"Run failed with status: {run.status}")
    
    async def cleanup(self):
        """Clean up resources."""
        if self.agent:
            print("\nCleaning up agent...")
            await self.client.agents.delete_agent(self.agent.id)
        
        if self.thread:
            print("Cleaning up thread...")
            await self.client.agents.delete_thread(self.thread.id)

async def main():
    """Main function to demonstrate the data analysis agent."""
    agent = DataAnalysisAgent()
    
    try:
        # Create agent
        await agent.create_agent()
        
        # Upload data file
        data_file = "../data/sales_data.csv"
        if os.path.exists(data_file):
            uploaded_file = await agent.upload_file(data_file)
            
            # Create thread with file
            await agent.create_thread_with_file(uploaded_file.id)
            
            # Analyze data with different prompts
            prompts = [
                "Please analyze this sales data and provide a summary of key insights.",
                "Create a bar chart showing total sales by product across all regions.",
                "Generate a line chart showing sales trends over time for each product.",
                "Which region and product combination has the highest sales? Create a visualization to show this."
            ]
            
            for prompt in prompts:
                await agent.analyze_data(prompt)
                await asyncio.sleep(3)  # Brief pause between analyses
        else:
            print(f"Data file not found: {data_file}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Cleanup
        await agent.cleanup()
        print("\nAgent session completed.")

if __name__ == "__main__":
    asyncio.run(main())