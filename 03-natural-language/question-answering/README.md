# Azure AI Question Answering Lab

## Building Conversational AI with Azure AI Language Question Answering

This lab demonstrates how to create intelligent conversational experiences using Azure AI Language's Question Answering service.

### 🎯 Learning Objectives

- Understand Azure AI Language Question Answering capabilities
- Create and manage knowledge bases from various sources
- Deploy question answering models
- Build client applications to query knowledge bases
- Implement best practices for conversational AI

### 📋 Prerequisites

- Azure subscription
- Python 3.8+
- Azure AI Language resource with Question Answering enabled

### 🏗️ Architecture

```
Data Sources → Language Studio → Knowledge Base → Deploy → API Endpoint
     ↓                                                         ↓
FAQ URLs                                               Python Client App
Manual Q&A                                                    ↓
Chit-chat                                               User Questions
```

### 🚀 Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/aihearticu/azure-ai-question-answering-lab.git
   cd azure-ai-question-answering-lab
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure credentials
   ```

4. **Run the application**
   ```bash
   python src/qna-app.py
   ```

### 📁 Project Structure

```
azure-ai-question-answering-lab/
├── README.md
├── requirements.txt
├── .env.example
├── src/
│   └── qna-app.py
├── docs/
│   ├── setup-guide.md
│   └── api-reference.md
└── tests/
    └── test_qna.py
```

### 💡 Key Features

- **Knowledge Base Import**: Import from URLs, files, or manual entries
- **Chit-chat Integration**: Add personality to your bot
- **Multi-turn Conversations**: Support follow-up questions
- **Active Learning**: Improve accuracy over time
- **Confidence Scoring**: Evaluate answer quality

### 🔧 Configuration

Create a `.env` file with your Azure credentials:

```env
AI_SERVICE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AI_SERVICE_KEY=your-api-key
QA_PROJECT_NAME=LearnFAQ
QA_DEPLOYMENT_NAME=production
```

### 📊 Sample Output

```
Question: What is Microsoft Learn?
Answer: Microsoft Learn is a free, online training platform that provides interactive learning paths...
Confidence: 0.95

Question: How do I get started?
Answer: To get started with Microsoft Learn, visit learn.microsoft.com and...
Confidence: 0.87
```

### 🛠️ Advanced Usage

```python
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.core.credentials import AzureKeyCredential

# Initialize client
client = QuestionAnsweringClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# Query with options
response = client.get_answers(
    question="What is Azure?",
    project_name=project,
    deployment_name=deployment,
    top=3,  # Get top 3 answers
    confidence_threshold=0.7  # Minimum confidence
)
```

### 📈 Best Practices

1. **Knowledge Base Design**
   - Start with existing FAQ content
   - Add question variations
   - Use follow-up prompts for complex topics
   - Regular updates based on user feedback

2. **Testing Strategy**
   - Test in Language Studio first
   - Verify confidence scores
   - Handle "no answer found" gracefully
   - Monitor usage analytics

3. **Security**
   - Use environment variables for credentials
   - Implement authentication for production
   - Monitor API usage and costs

### 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Low confidence scores | Add more question variations |
| Wrong answers | Check for conflicting Q&A pairs |
| Slow responses | Optimize knowledge base size |
| No answers found | Lower confidence threshold or add more content |

### 💰 Cost Optimization

- **Free tier**: 1,000 transactions/month
- **Standard tier**: Pay per transaction
- Use caching for repeated questions
- Monitor usage in Azure Portal

### 🎯 Real-World Applications

- Customer support chatbots
- Internal knowledge bases
- Documentation assistants
- FAQ automation
- Virtual help desks

### 📚 Resources

- [Azure AI Language Documentation](https://docs.microsoft.com/azure/cognitive-services/language-service/)
- [Question Answering Quickstart](https://docs.microsoft.com/azure/cognitive-services/language-service/question-answering/quickstart)
- [Language Studio](https://language.cognitive.azure.com/)

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

### 🌟 Acknowledgments

- Microsoft Learn for FAQ content
- Azure AI Language team for the service
- Community contributors

---

**Created with ❤️ by AIHeartICU**