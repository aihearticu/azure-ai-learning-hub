import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from typing import Dict, List, Optional
import requests
from datetime import datetime

# Load environment variables
load_dotenv()

class MCPServer:
    """Simulated MCP Server for documentation search."""
    
    def __init__(self):
        # Simulated documentation database
        self.documentation = {
            "azure_openai": {
                "title": "Azure OpenAI Service",
                "content": """Azure OpenAI Service provides REST API access to OpenAI's powerful language models.
                
Key Features:
- GPT-4 and GPT-3.5 models
- DALL-E for image generation
- Whisper for speech-to-text
- Enterprise security and compliance

Getting Started:
1. Create an Azure OpenAI resource
2. Deploy a model
3. Use the REST API or SDKs

Example code:
```python
from openai import AzureOpenAI
client = AzureOpenAI(
    azure_endpoint="https://your-resource.openai.azure.com/",
    api_key="your-api-key",
    api_version="2024-02-15-preview"
)
```""",
                "last_updated": "2024-12-15",
                "tags": ["azure", "openai", "ai", "gpt"]
            },
            "semantic_kernel": {
                "title": "Semantic Kernel SDK",
                "content": """Semantic Kernel is an open-source SDK that lets you easily build agents that can call your existing code.

Key Concepts:
- Plugins: Encapsulate capabilities
- Functions: Individual operations
- Memory: Store and retrieve information
- Planners: Orchestrate complex tasks

Installation:
```bash
pip install semantic-kernel
```

Basic Usage:
```python
import semantic_kernel as sk
kernel = sk.Kernel()
# Add plugins and functions
```""",
                "last_updated": "2024-12-10",
                "tags": ["semantic-kernel", "sdk", "agents", "ai"]
            },
            "azure_ai_agents": {
                "title": "Azure AI Agent Service",
                "content": """Azure AI Agent Service enables building sophisticated AI agents with tool use capabilities.

Features:
- Multi-agent orchestration
- Custom function integration
- Code interpreter
- File search
- MCP tool support

Creating an Agent:
```python
from azure.ai.agents import AgentsClient
client = AgentsClient(endpoint, credential)
agent = client.create_agent(
    model="gpt-4",
    tools=[...],
    instructions="..."
)
```""",
                "last_updated": "2024-12-20",
                "tags": ["agents", "azure", "ai", "tools"]
            },
            "mcp_protocol": {
                "title": "Model Context Protocol (MCP)",
                "content": """MCP enables AI agents to connect to external data sources and tools.

Benefits:
- Real-time data access
- Standardized tool interface
- Secure connections
- Scalable architecture

Implementation:
1. Set up MCP server
2. Define available tools
3. Connect agents to server
4. Handle tool requests

Security:
- Authentication required
- Encrypted connections
- Access control per tool""",
                "last_updated": "2024-12-18",
                "tags": ["mcp", "protocol", "tools", "integration"]
            }
        }
    
    def search(self, query: str, tags: List[str] = None) -> List[Dict]:
        """Search documentation based on query and optional tags."""
        results = []
        query_lower = query.lower()
        
        for key, doc in self.documentation.items():
            # Check if query matches title or content
            if (query_lower in doc['title'].lower() or 
                query_lower in doc['content'].lower()):
                
                # Check tags if provided
                if tags:
                    if any(tag in doc['tags'] for tag in tags):
                        results.append({
                            "id": key,
                            "title": doc['title'],
                            "preview": doc['content'][:200] + "...",
                            "tags": doc['tags'],
                            "last_updated": doc['last_updated']
                        })
                else:
                    results.append({
                        "id": key,
                        "title": doc['title'],
                        "preview": doc['content'][:200] + "...",
                        "tags": doc['tags'],
                        "last_updated": doc['last_updated']
                    })
        
        return results
    
    def get_document(self, doc_id: str) -> Optional[Dict]:
        """Get full document by ID."""
        return self.documentation.get(doc_id)

class DocumentationAgent:
    """AI Agent with MCP tool integration for documentation search."""
    
    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version="2024-02-15-preview"
        )
        self.deployment_name = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
        
        # Initialize simulated MCP server
        self.mcp_server = MCPServer()
        
        # Define MCP tool functions
        self.functions = [
            {
                "type": "function",
                "function": {
                    "name": "search_documentation",
                    "description": "Search Microsoft documentation using MCP server",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query for documentation"
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional tags to filter results"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_documentation",
                    "description": "Retrieve full documentation by ID",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "doc_id": {
                                "type": "string",
                                "description": "Documentation ID to retrieve"
                            }
                        },
                        "required": ["doc_id"]
                    }
                }
            }
        ]
        
        self.system_prompt = """You are a Documentation Assistant Agent with access to an MCP server containing Microsoft documentation.

Your capabilities:
1. Search for relevant documentation using the MCP server
2. Provide accurate, up-to-date information from official sources
3. Help developers find the right guidance for their tasks
4. Explain complex concepts clearly

When users ask questions:
1. Search the documentation first
2. Provide specific, relevant excerpts
3. Include code examples when available
4. Cite the source and last update date
5. Offer to search for related topics

Always prioritize accuracy and cite your sources."""
        
        self.messages = [{"role": "system", "content": self.system_prompt}]
    
    def search_documentation(self, query: str, tags: List[str] = None) -> str:
        """MCP tool: Search documentation."""
        results = self.mcp_server.search(query, tags)
        
        if results:
            response = {
                "status": "success",
                "count": len(results),
                "results": results
            }
        else:
            response = {
                "status": "no_results",
                "message": f"No documentation found for '{query}'"
            }
        
        return json.dumps(response)
    
    def get_documentation(self, doc_id: str) -> str:
        """MCP tool: Get full documentation."""
        doc = self.mcp_server.get_document(doc_id)
        
        if doc:
            response = {
                "status": "success",
                "document": doc
            }
        else:
            response = {
                "status": "not_found",
                "message": f"Document '{doc_id}' not found"
            }
        
        return json.dumps(response)
    
    def process_query(self, user_query: str) -> str:
        """Process user query using AI and MCP tools."""
        # Add user query to messages
        self.messages.append({"role": "user", "content": user_query})
        
        # Get AI response with tool use
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=self.messages,
            tools=self.functions,
            tool_choice="auto",
            temperature=0.7,
            max_tokens=800
        )
        
        assistant_message = response.choices[0].message
        
        # Process tool calls if any
        if assistant_message.tool_calls:
            self.messages.append(assistant_message)
            
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute MCP tool
                if function_name == "search_documentation":
                    result = self.search_documentation(**function_args)
                elif function_name == "get_documentation":
                    result = self.get_documentation(**function_args)
                else:
                    result = json.dumps({"error": f"Unknown function: {function_name}"})
                
                # Add tool result
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # Get final response
            final_response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=self.messages,
                temperature=0.7,
                max_tokens=800
            )
            
            final_message = final_response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": final_message})
            
            return final_message
        else:
            self.messages.append({"role": "assistant", "content": assistant_message.content})
            return assistant_message.content

def main():
    """Main function to demonstrate MCP-enabled documentation agent."""
    print("=== Documentation Agent with MCP Tools ===")
    print("Ask questions about Azure AI services and Microsoft tools.")
    print("Type 'quit' to exit.\n")
    
    agent = DocumentationAgent()
    
    # Initial greeting
    print("Agent: Hello! I'm your documentation assistant with access to Microsoft's documentation through MCP.")
    print("I can help you find information about:")
    print("- Azure OpenAI Service")
    print("- Semantic Kernel SDK")
    print("- Azure AI Agents")
    print("- Model Context Protocol (MCP)")
    print("\nWhat would you like to know?\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("Agent: Goodbye! Happy coding!")
            break
        
        # Process query
        response = agent.process_query(user_input)
        print(f"\nAgent: {response}\n")

def demo_mode():
    """Run demonstration of MCP tool capabilities."""
    print("=== MCP Documentation Agent Demo ===\n")
    
    agent = DocumentationAgent()
    
    # Demo queries
    queries = [
        "How do I get started with Azure OpenAI?",
        "What is Semantic Kernel and how do I install it?",
        "Tell me about the Model Context Protocol",
        "How can I create an AI agent with custom tools?",
        "What are the security considerations for MCP?"
    ]
    
    for query in queries:
        print(f"User: {query}")
        response = agent.process_query(query)
        print(f"\nAgent: {response}\n")
        print("-" * 80 + "\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_mode()
    else:
        main()