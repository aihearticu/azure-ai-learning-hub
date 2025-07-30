# Agent Orchestration - Multi-Agent System Lab

This module implements the Microsoft Learn lab for creating a multi-agent system using Semantic Kernel SDK.

## Overview

This lab demonstrates:
- Creating multiple specialized AI agents
- Orchestrating conversations between agents
- Implementing selection strategies for agent turns
- Building termination strategies for conversations
- Analyzing log files for incident management

## Architecture

The system consists of two specialized agents:

1. **Incident Manager Agent**
   - Analyzes log files for issues
   - Determines incident severity
   - Coordinates with DevOps for resolution
   - Provides status updates

2. **DevOps Assistant Agent**
   - Implements technical solutions
   - Performs system operations
   - Provides technical analysis
   - Reports completion status

## Setup

1. **Install Dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   - Update `.env` with your Azure OpenAI credentials

3. **Run the Multi-Agent System**:
   ```bash
   cd src
   python multi_agent_demo.py
   ```

## Features

- **Log Analysis**: Agents analyze different types of log entries
- **Dynamic Conversation**: Agents take turns based on context
- **Problem Resolution**: Agents work together to resolve incidents
- **Multiple Scenarios**: Test with different log patterns:
  - Critical database errors
  - Performance degradation
  - Normal operation

## Sample Log Files

The `data/` directory contains sample log files:
- `critical_error.log`: Database connection failures
- `performance_issue.log`: High response times and resource usage
- `normal_operation.log`: Healthy system metrics

## How It Works

1. **Incident Manager** analyzes logs and identifies issues
2. If action is needed, **DevOps Assistant** implements solutions
3. **Incident Manager** verifies the resolution
4. Conversation continues until issue is resolved or no action needed

## Key Components

- `multi_agent_demo.py`: Main orchestration implementation
- `MultiAgentOrchestrator`: Manages agent conversations
- Selection logic: Determines which agent speaks next
- Termination logic: Ends conversation when appropriate

## Example Interaction

```
[IncidentManager]:
I've analyzed the logs and identified a critical issue...

[DevOpsAssistant]:
I'll implement the following solutions...

[IncidentManager]:
The issue has been resolved. All systems are operational.
```

## Key Learnings

- Multi-agent systems can handle complex workflows
- Specialized agents improve problem-solving efficiency
- Orchestration strategies control conversation flow
- Azure OpenAI enables sophisticated agent behaviors

## Reference

Based on: [Microsoft Learn - Agent Orchestration Lab](https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/05-agent-orchestration.html)