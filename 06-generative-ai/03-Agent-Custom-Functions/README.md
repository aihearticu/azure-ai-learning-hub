# Exercise 03: Agent Custom Functions

This exercise demonstrates creating an AI agent with custom function capabilities for technical support.

## Overview

The Technical Support Agent can:
- Search knowledge base articles
- Submit support tickets
- Check ticket status
- Escalate urgent issues
- Interact naturally with customers

## Features

### Custom Functions
1. **submit_support_ticket** - Create new support tickets
2. **check_ticket_status** - Check existing ticket status
3. **escalate_ticket** - Escalate tickets to higher priority
4. **get_knowledge_base_article** - Search knowledge base

### Agent Capabilities
- Natural language understanding
- Automatic function selection
- Context-aware responses
- Professional support interactions

## Setup

1. **Install Dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   - Copy `.env.example` to `.env`
   - Add your Azure OpenAI credentials

3. **Run the Agent**:
   ```bash
   cd src
   python support_agent.py        # Interactive mode
   python support_agent.py demo   # Demo mode
   ```

## Implementation Details

### Custom Functions (`user_functions.py`)
- Implements all support operations
- Stores tickets as text files
- Returns JSON responses
- Includes simulated knowledge base

### Support Agent (`support_agent.py`)
- Uses Azure OpenAI with function calling
- Maintains conversation context
- Automatically selects appropriate functions
- Provides helpful support interactions

## Usage Examples

### Interactive Mode
```
You: I can't connect to the VPN
Support Agent: I can help you with VPN connection issues. Let me search our knowledge base...

You: My email is broken and I need urgent help. My email is user@company.com
Support Agent: I understand this is urgent. Let me create a high-priority support ticket...
```

### Demo Mode
Runs through predefined scenarios showing:
- Knowledge base searches
- Ticket creation
- Status checking
- Ticket escalation

## Function Definitions

### submit_support_ticket
- **Parameters**: email_address, description, priority
- **Returns**: Ticket number and confirmation

### check_ticket_status
- **Parameters**: ticket_number
- **Returns**: Current ticket status

### escalate_ticket
- **Parameters**: ticket_number, reason
- **Returns**: Escalation confirmation

### get_knowledge_base_article
- **Parameters**: topic
- **Returns**: Relevant articles or search results

## File Structure
```
03-Agent-Custom-Functions/
├── src/
│   ├── support_agent.py      # Main agent implementation
│   └── user_functions.py     # Custom function implementations
├── data/
│   └── tickets/             # Stored support tickets
├── requirements.txt
├── .env.example
└── README.md
```

## Key Learnings

1. **Function Calling**: How to define and integrate custom functions with AI agents
2. **Tool Choice**: Letting the AI automatically select appropriate functions
3. **Context Management**: Maintaining conversation history for coherent interactions
4. **Error Handling**: Gracefully handling function execution and results

## Next Steps

- Add more custom functions (e.g., schedule callbacks, system diagnostics)
- Integrate with real ticketing systems
- Add authentication and user management
- Implement function result validation

## Reference

Based on: [Microsoft Learn - Agent Custom Functions](https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/03-agent-custom-functions.html)