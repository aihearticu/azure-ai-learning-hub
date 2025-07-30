# Semantic Kernel - Expense Agent Lab

This module implements the Microsoft Learn lab for creating an AI agent using Semantic Kernel SDK.

## Overview

This lab demonstrates:
- Creating an AI agent for expense claim processing
- Integrating Azure OpenAI with Semantic Kernel
- Implementing custom plugins (EmailPlugin)
- Building conversational AI experiences

## Setup

1. **Install Dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   - Copy `.env.example` to `.env`
   - Update with your Azure OpenAI credentials

3. **Run the Agent**:
   ```bash
   cd src
   python expense_agent.py
   ```

## Features

- **Expense Tracking**: The agent helps users input and track expenses
- **Validation Rules**: Enforces business rules for expense limits
- **Email Integration**: Simulates sending expense claims via email
- **Conversational Interface**: Natural language interaction for expense submission

## Key Components

- `expense_agent.py`: Main agent implementation
- `email_plugin.py`: Custom plugin for email functionality
- Uses Azure OpenAI GPT-4o model for natural language understanding

## Usage Example

1. Start the agent
2. Describe your expenses in natural language
3. The agent will help you categorize and validate expenses
4. Type 'done' to submit the expense claim
5. The agent will format and "send" an email with your expenses

## Key Learnings

- Semantic Kernel simplifies AI agent development
- Custom plugins extend agent capabilities
- Azure OpenAI integration provides powerful language understanding
- Conversational agents can handle complex business workflows

## Reference

Based on: [Microsoft Learn - Semantic Kernel Lab](https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/04-semantic-kernel.html)