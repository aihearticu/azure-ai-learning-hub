#!/usr/bin/env python3
"""Test script for the multi-agent orchestration"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_setup():
    """Test that all components are properly configured."""
    print("Testing Multi-Agent Orchestration Setup...")
    print("-" * 50)
    
    # Test environment variables
    required_vars = ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_DEPLOYMENT_NAME"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
        else:
            print(f"✓ {var} is configured")
    
    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("\n✓ All environment variables configured")
    
    # Test log files
    print("\nChecking sample log files...")
    log_dir = "../data"
    log_files = ["critical_error.log", "performance_issue.log", "normal_operation.log"]
    
    for log_file in log_files:
        path = os.path.join(log_dir, log_file)
        if os.path.exists(path):
            print(f"✓ {log_file} exists")
        else:
            print(f"❌ {log_file} not found")
    
    # Test imports
    print("\nTesting required imports...")
    try:
        from semantic_kernel import Kernel
        from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
        from semantic_kernel.contents.chat_history import ChatHistory
        print("✓ All imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    print("\n✅ All tests passed! The multi-agent system is ready.")
    print("\nTo run the full orchestration, execute: python multi_agent_demo.py")
    return True

if __name__ == "__main__":
    asyncio.run(test_setup())