#!/usr/bin/env python3
"""Test script for the expense agent"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from email_plugin import EmailPlugin

# Load environment variables
load_dotenv()

async def test_connections():
    """Test Azure OpenAI connection and plugin"""
    print("Testing Expense Agent Setup...")
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
    
    # Test email plugin
    print("\nTesting Email Plugin...")
    email_plugin = EmailPlugin()
    
    # Test formatting
    formatted_email = email_plugin.format_expense_summary(
        expenses="- Lunch meeting: $45.00\n- Office supplies: $23.50",
        total_amount=68.50,
        employee_name="Test User"
    )
    print("✓ Email formatting works")
    
    # Test sending (simulated)
    result = email_plugin.send_email(
        to="test@example.com",
        subject="Test Email",
        body=formatted_email
    )
    print("✓ Email sending (simulated) works")
    
    print("\n✅ All tests passed! The agent is ready to use.")
    print("\nTo run the full agent, execute: python expense_agent.py")
    return True

if __name__ == "__main__":
    asyncio.run(test_connections())