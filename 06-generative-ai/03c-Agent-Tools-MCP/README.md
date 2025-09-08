# Exercise 03c: Use Agent Tools with MCP

This exercise demonstrates integrating Model Context Protocol (MCP) tools with AI agents for real-time documentation access.

## Overview

MCP (Model Context Protocol) enables AI agents to:
- Connect to cloud-hosted servers
- Access real-time documentation
- Retrieve up-to-date information
- Provide accurate guidance on Microsoft tools

## What is MCP?

Model Context Protocol is a standardized way for AI agents to interact with external data sources and tools. It provides:
- Secure connections to data servers
- Standardized command interface
- Real-time data access
- Authentication and access control

## Implementation

### 1. Documentation Agent (`mcp_documentation_agent.py`)
Full-featured agent with simulated MCP server including:
- Documentation search functionality
- Content retrieval
- AI-powered query processing
- Source citation

### 2. MCP Integration (`mcp_integration.py`)
Demonstrates core MCP concepts:
- Tool registry
- Protocol handler
- Connection management
- Command execution

## Setup

1. **Install Dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   - Copy `.env.example` to `.env`
   - Add Azure OpenAI credentials
   - Configure MCP server details (simulated)

3. **Run Examples**:
   ```bash
   cd src
   # Interactive documentation agent
   python mcp_documentation_agent.py
   
   # Demo mode
   python mcp_documentation_agent.py demo
   
   # MCP integration demonstration
   python mcp_integration.py
   ```

## MCP Tool Capabilities

### Available Tools
1. **Documentation Server**
   - Search Microsoft docs
   - Retrieve full articles
   - Access update timestamps

2. **Code Samples** (simulated)
   - Find example code
   - Download samples
   - Validate syntax

3. **API Reference** (simulated)
   - Look up API schemas
   - Get usage examples
   - Check parameters

4. **Troubleshooting** (simulated)
   - Diagnose issues
   - Find solutions
   - Check known issues

## Usage Examples

### Documentation Search
```
You: How do I get started with Azure OpenAI?
Agent: Let me search the documentation for you...
[Searches MCP server]
Agent: I found the official guide. Here's how to get started...
```

### Code Examples
```
You: Show me how to use Semantic Kernel
Agent: Searching for Semantic Kernel examples...
[Retrieves from MCP server]
Agent: Here's a basic example with installation instructions...
```

## Key Features

1. **Real-time Access**: Always gets latest documentation
2. **Source Citation**: Provides references and update dates
3. **Intelligent Search**: AI-enhanced query understanding
4. **Multi-tool Support**: Can access multiple MCP servers
5. **Secure Connections**: Authentication and encryption

## Architecture

```
User Query
    ↓
AI Agent
    ↓
MCP Tool Selection
    ↓
MCP Server Connection
    ↓
Command Execution
    ↓
Result Processing
    ↓
AI Response Generation
```

## MCP Protocol Flow

1. **Connection Phase**
   - Authenticate with server
   - Establish session
   - Get capabilities

2. **Command Phase**
   - Send search/retrieve commands
   - Handle responses
   - Process results

3. **Disconnection Phase**
   - Close session
   - Clean up resources

## File Structure
```
03c-Agent-Tools-MCP/
├── src/
│   ├── mcp_documentation_agent.py  # Full agent implementation
│   └── mcp_integration.py         # MCP protocol demonstration
├── data/                          # Data storage
├── requirements.txt
├── .env.example
└── README.md
```

## Key Learnings

1. **Protocol Integration**: How MCP standardizes tool access
2. **Real-time Data**: Accessing live documentation vs static
3. **Tool Orchestration**: AI agents selecting appropriate tools
4. **Security Model**: Authentication and secure connections
5. **Scalability**: Adding new MCP servers and capabilities

## Production Considerations

1. **Authentication**: Implement proper OAuth/API key handling
2. **Caching**: Cache frequent queries for performance
3. **Error Handling**: Graceful fallback when servers unavailable
4. **Rate Limiting**: Respect server rate limits
5. **Monitoring**: Track MCP tool usage and performance

## Next Steps

- Connect to real MCP servers when available
- Implement custom MCP servers for internal docs
- Add more tool types (databases, APIs, etc.)
- Create MCP adapters for existing systems
- Build MCP tool discovery mechanisms

## Reference

Based on: [Microsoft Learn - Use Agent Tools with MCP](https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/03c-use-agent-tools-with-mcp.html)

Note: MCP is in preview. This implementation uses simulated servers for demonstration purposes.