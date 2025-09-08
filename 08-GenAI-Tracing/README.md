# Lab 08: Tracing GenAI Applications

## Overview
This lab demonstrates how to implement distributed tracing for generative AI applications using Azure OpenAI and Application Insights. You'll build a hiking trail recommendation system with comprehensive observability.

## Objectives
- Implement OpenTelemetry tracing in a GenAI application
- Connect Azure OpenAI with Application Insights
- Debug AI applications using distributed traces
- Monitor performance and optimize model interactions

## Prerequisites
- Azure subscription
- Python 3.8+
- Azure CLI installed and configured

## Key Learnings
1. **Distributed Tracing**: Instrument AI applications for complete observability
2. **Error Debugging**: Use traces to identify and resolve issues
3. **Performance Monitoring**: Track model latency and token usage
4. **Best Practices**: Implement proper span attributes and error handling

## Architecture

```
User Input → Hiking Assistant → Azure OpenAI (GPT-4o)
                ↓
        OpenTelemetry Traces
                ↓
        Application Insights → Azure Monitor
```

## Setup Instructions

### 1. Create Azure Resources
```bash
# Create resource group
az group create --name rg-genai-tracing --location eastus

# Create Azure OpenAI resource
az cognitiveservices account create \
  --name openai-genai-tracing-$RANDOM \
  --resource-group rg-genai-tracing \
  --kind OpenAI \
  --sku S0 \
  --location eastus \
  --yes

# Create Application Insights
az monitor app-insights component create \
  --app app-insights-genai-tracing \
  --location eastus \
  --resource-group rg-genai-tracing \
  --application-type web

# Deploy GPT-4o model
az cognitiveservices account deployment create \
  --name <your-openai-resource> \
  --resource-group rg-genai-tracing \
  --deployment-name gpt-4o \
  --model-name gpt-4o \
  --model-version 2024-08-06 \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name Standard
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install python-dotenv openai azure-identity \
  azure-ai-projects opentelemetry-instrumentation-openai \
  azure-monitor-opentelemetry-exporter
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and update with your values:
```bash
AZURE_OPENAI_ENDPOINT=<your-endpoint>
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
APPLICATIONINSIGHTS_CONNECTION_STRING=<your-connection-string>
```

## Running the Application

### Main Application
```bash
python src/hiking_assistant.py
```

The application will:
1. Ask for your hiking preferences
2. Recommend suitable trails
3. Generate a trip profile with gear recommendations
4. Match gear with product catalog
5. Send traces to Application Insights

### Error Tracing Demo
```bash
python src/hiking_assistant_with_error.py
```

This demonstrates how errors appear in distributed traces.

## Code Structure

### `hiking_assistant.py`
Main application with the following components:
- **configure_tracing()**: Sets up OpenTelemetry with Azure Monitor
- **call_ai_model()**: Wrapped OpenAI calls with tracing
- **recommend_hikes()**: Generates trail recommendations
- **generate_trip_profile()**: Creates personalized trip plans
- **match_products()**: Maps gear to product catalog

### Key Tracing Patterns

```python
# Creating spans
with tracer.start_as_current_span("operation_name") as span:
    # Set attributes
    span.set_attribute("user.location", location)
    
    # Record events
    span.add_event("Processing started")
    
    # Handle errors
    try:
        result = perform_operation()
    except Exception as e:
        span.record_exception(e)
        span.set_status(Status(StatusCode.ERROR, str(e)))
        raise
```

## Viewing Traces

1. Navigate to Azure Portal
2. Open your Application Insights resource
3. Go to "Transaction Search" or "Application Map"
4. Filter by time range to see your traces
5. Click on individual operations to see detailed spans

## Trace Analysis

Look for:
- **Latency**: Which operations take the longest?
- **Errors**: Where do failures occur?
- **Dependencies**: How do components interact?
- **Attributes**: What context is captured?

## Best Practices

### Tracing
- Use semantic naming for spans
- Add relevant attributes for filtering
- Record exceptions with context
- Implement sampling for production

### Security
- Never log sensitive data (API keys, PII)
- Use managed identities when possible
- Implement proper RBAC

### Performance
- Cache frequently used responses
- Implement retry logic
- Monitor token usage

## Troubleshooting

### No traces appearing
- Check Application Insights connection string
- Verify network connectivity
- Allow time for data ingestion (1-2 minutes)

### JSON parsing errors
- Check model response format
- Implement fallback parsing logic
- Log raw responses for debugging

## Clean Up

```bash
# Delete all resources
az group delete --name rg-genai-tracing --yes --no-wait
```

## Additional Resources
- [Microsoft Learn Lab](https://microsoftlearning.github.io/mslearn-genaiops/Instructions/08-Tracing-GenAI-application.html)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Azure Monitor OpenTelemetry](https://learn.microsoft.com/azure/azure-monitor/app/opentelemetry-overview)

## Lab Completion
✅ You've successfully implemented distributed tracing for a GenAI application!

Key achievements:
- Built a functional AI assistant with tracing
- Integrated Azure OpenAI with Application Insights  
- Implemented comprehensive error handling
- Created observable, debuggable AI applications