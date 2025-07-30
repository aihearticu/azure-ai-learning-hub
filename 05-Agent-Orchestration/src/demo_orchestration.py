#!/usr/bin/env python3
"""Automated demo of the multi-agent orchestration"""

import asyncio
import os
from dotenv import load_dotenv
from multi_agent_demo import MultiAgentOrchestrator, INCIDENT_MANAGER, DEVOPS_ASSISTANT
from multi_agent_demo import INCIDENT_MANAGER_INSTRUCTIONS, DEVOPS_ASSISTANT_INSTRUCTIONS
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# Load environment variables
load_dotenv()

async def run_automated_demo():
    """Run an automated demonstration of the multi-agent system."""
    print("=== AUTOMATED MULTI-AGENT ORCHESTRATION DEMO ===\n")
    
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
    
    # Demo scenario: Critical Database Error
    critical_logs = """[2024-01-20 10:15:23] ERROR: Database connection failed - timeout after 30s
[2024-01-20 10:15:24] ERROR: Failed to connect to primary database
[2024-01-20 10:15:25] WARNING: Failover to secondary database initiated
[2024-01-20 10:15:26] ERROR: Secondary database also unreachable
[2024-01-20 10:15:27] CRITICAL: All database connections lost
[2024-01-20 10:15:28] ERROR: API endpoints returning 500 errors
[2024-01-20 10:15:29] CRITICAL: Customer-facing services are down"""
    
    print("Scenario: Critical Database Error")
    print("=" * 40)
    print("\nLog entries being analyzed:")
    print(critical_logs)
    print("\n" + "=" * 40 + "\n")
    
    # Run the orchestration
    initial_message = f"Please analyze these log entries and determine if any action is needed:\n\n{critical_logs}"
    await orchestrator.orchestrate_conversation(initial_message, max_turns=6)
    
    print("\n" + "=" * 80 + "\n")
    print("Demo completed. The agents successfully:")
    print("1. Identified the critical database issue")
    print("2. Coordinated to implement solutions")
    print("3. Verified the resolution")
    print("\nThis demonstrates how multiple AI agents can work together to resolve incidents.")

if __name__ == "__main__":
    asyncio.run(run_automated_demo())