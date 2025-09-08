# Azure AI Foundry Evaluators Reference Guide 📊

**Complete reference for implementing agent observability with Azure AI Foundry evaluators**

## Overview

Azure AI Foundry provides comprehensive evaluators to assess AI agent performance across multiple dimensions. These evaluators are essential for implementing the 5 observability best practices from the Agent Factory series.

## 🤖 Agent-Specific Evaluators

### 1. Intent Resolution Evaluator

**Purpose**: Measures how well the system identifies and understands a user's request

**Reference**: [Microsoft Docs - Intent Resolution](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators#intent-resolution)

**Key Features**:
- Evaluates scoping of user intent
- Assesses clarifying question capability
- Measures system capability awareness
- Uses Likert scale 1-5 (higher = better)
- Default threshold: 3

**Implementation**:
```python
from azure.ai.evaluation import IntentResolutionEvaluator

intent_resolution = IntentResolutionEvaluator(
    model_config=model_config, 
    threshold=3
)

result = intent_resolution(
    query="What are the opening hours of the Eiffel Tower?",
    response="Opening hours of the Eiffel Tower are 9:00 AM to 11:00 PM."
)
```

**Output Structure**:
```json
{
    "intent_resolution": 4.0,
    "intent_resolution_result": "pass",
    "intent_resolution_threshold": 3,
    "intent_resolution_reason": "The response directly addresses..."
}
```

### 2. Tool Call Accuracy Evaluator

**Purpose**: Measures accuracy and efficiency of tool calls made by AI agents

**Reference**: [Microsoft Docs - Tool Call Accuracy](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators#tool-call-accuracy)

**Key Features**:
- Evaluates tool invocation relevance
- Assesses parameter correctness
- Identifies missing/excessive tool calls
- Supports Azure AI Agent Function Tools only
- Uses Likert scale 1-5

**Implementation**:
```python
from azure.ai.evaluation import ToolCallAccuracyEvaluator

tool_call_accuracy = ToolCallAccuracyEvaluator(
    model_config=model_config, 
    threshold=3
)

result = tool_call_accuracy(
    query="How is the weather in Seattle?",
    tool_calls=[...],
    tool_definitions=[...]
)
```

**Requirements**:
- At least one Function Tool call required
- Does not support Built-in Tool evaluation

### 3. Task Adherence Evaluator

**Purpose**: Measures how well an agent's response adheres to assigned tasks

**Reference**: [Microsoft Docs - Task Adherence](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators#task-adherence)

**Key Features**:
- Evaluates alignment with task instructions
- Measures efficiency of steps taken
- Assesses scope adherence
- Checks response comprehensiveness
- Uses Likert scale 1-5

**Implementation**:
```python
from azure.ai.evaluation import TaskAdherenceEvaluator

task_adherence = TaskAdherenceEvaluator(
    model_config=model_config, 
    threshold=3
)

result = task_adherence(
    query="What are the best practices for maintaining a healthy rose garden?",
    response="Make sure to water your roses regularly and trim them occasionally."
)
```

## 🔍 RAG System Evaluators

### 4. Relevance Evaluator

**Purpose**: Measures how effectively a response addresses a query

**Reference**: [Microsoft Docs - Relevance](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/rag-evaluators#relevance)

**Key Features**:
- Assesses accuracy and completeness
- Evaluates direct relevance to query
- Uses Likert scale 1-5
- Provides detailed reasoning

**Implementation**:
```python
from azure.ai.evaluation import RelevanceEvaluator

relevance = RelevanceEvaluator(
    model_config=model_config, 
    threshold=3
)

result = relevance(
    query="Is Marie Curie born in Paris?",
    response="No, Marie Curie was born in Warsaw."
)
```

## 📝 General Purpose Evaluators

### 5. Coherence Evaluator

**Purpose**: Measures logical and orderly presentation of ideas

**Reference**: [Microsoft Docs - Coherence](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/general-purpose-evaluators#coherence)

**Key Features**:
- Evaluates logical sequence
- Assesses connection between sentences
- Measures thought process clarity
- Uses appropriate transitions
- Uses Likert scale 1-5

**Implementation**:
```python
from azure.ai.evaluation import CoherenceEvaluator

coherence = CoherenceEvaluator(
    model_config=model_config, 
    threshold=3
)

result = coherence(
    query="Is Marie Curie born in Paris?",
    response="No, Marie Curie was born in Warsaw."
)
```

### 6. Fluency Evaluator

**Purpose**: Measures effectiveness and clarity of written communication

**Reference**: [Microsoft Docs - Fluency](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/general-purpose-evaluators#fluency)

**Key Features**:
- Evaluates grammatical accuracy
- Assesses vocabulary range
- Measures sentence complexity
- Evaluates overall readability
- Uses Likert scale 1-5

**Implementation**:
```python
from azure.ai.evaluation import FluencyEvaluator

fluency = FluencyEvaluator(
    model_config=model_config, 
    threshold=3
)

result = fluency(
    response="No, Marie Curie was born in Warsaw."
)
```

## 🛡️ Risk and Safety Evaluators

**Purpose**: Comprehensive safety and risk assessment across multiple categories

**Reference**: [Microsoft Docs - Risk Safety Evaluators](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/risk-safety-evaluators)

### Available Safety Evaluators:

1. **Hateful and Unfair Content Evaluator**
2. **Sexual Content Evaluator**
3. **Violent Content Evaluator**
4. **Self-Harm Related Content Evaluator**
5. **Protected Material Content Evaluator**
6. **Direct Attack Jailbreak Evaluator**
7. **Indirect Attack Jailbreak Evaluator**
8. **Code Vulnerability Evaluator**
9. **Ungrounded Attributes Evaluator**

### Key Features:
- Uses 0-7 severity scale
- Calculates aggregate defect rate
- Provides detailed reasoning
- Supports multiple Azure regions
- Available as composite evaluator

### Implementation:
```python
from azure.ai.evaluation import ContentSafetyEvaluator

content_safety = ContentSafetyEvaluator(
    project_scope=project_scope
)

result = content_safety(
    query="Your query here",
    response="AI response to evaluate"
)
```

### Supported Regions:
- **Primary**: East US 2 (most comprehensive)
- **Secondary**: Sweden Central, US North Central, France Central, Switzerland West

## 🔧 Model Configuration

### Standard Model Config:
```python
model_config = {
    "azure_endpoint": "https://your-endpoint.openai.azure.com/",
    "azure_deployment": "gpt-4o",
    "api_version": "2024-02-15-preview",
    "api_key": "your-api-key"
}
```

### Project Scope (for Safety Evaluators):
```python
project_scope = {
    "subscription_id": "your-subscription-id",
    "resource_group_name": "your-resource-group",
    "project_name": "your-ai-foundry-project"
}
```

## 📊 Scoring Guidelines

### Likert Scale Interpretation:
- **5**: Excellent - Exceeds expectations
- **4**: Good - Meets expectations well
- **3**: Satisfactory - Meets basic expectations (default threshold)
- **2**: Below expectations - Needs improvement
- **1**: Poor - Significant issues

### Safety Scale (0-7):
- **0**: No issues detected
- **1-2**: Very Low severity
- **3-4**: Low-Medium severity
- **5-6**: High severity
- **7**: Very High severity

## 🚀 Best Practices

### 1. Model Selection
- Use **reasoning models** (o3-mini) for complex evaluations
- Use **non-reasoning models** (GPT-4o) for standard evaluations
- Consider cost vs. accuracy tradeoffs

### 2. Threshold Configuration
- Start with default threshold (3)
- Adjust based on business requirements
- Monitor pass/fail rates over time

### 3. Batch Evaluation
- Combine multiple evaluators for comprehensive assessment
- Use async processing for large datasets
- Implement caching for repeated evaluations

### 4. Regional Considerations
- Use East US 2 for full safety evaluator support
- Consider latency for real-time evaluations
- Plan for regional availability

## 🔗 Additional Resources

- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Azure AI Foundry Python SDK](https://pypi.org/project/azure-ai-evaluation/)
- [Azure AI Foundry GitHub Samples](https://github.com/Azure-Samples/azure-ai-foundry-samples)

---

*This reference guide supports the Agent Factory learning series Part 3: Observability Best Practices*