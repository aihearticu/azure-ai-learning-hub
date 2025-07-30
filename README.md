# Azure AI Learning Hub

This repository contains hands-on implementations and documentation from the Microsoft Azure AI Engineer (AI-102) certification journey.

## 📈 Learning Progress

**10 of 24 Modules Completed (41.7%)** - See [LEARNING_PROGRESS.md](./LEARNING_PROGRESS.md) for detailed tracking

## 🚀 Repository Structure

```
Azure-AI-Learning-Modules/
├── 01-fundamentals/             # Azure AI Services basics
├── 02-computer-vision/          # Computer Vision services
├── 03-natural-language/         # Language and Speech services
│   ├── 05-Custom-Entity-Extraction/
│   ├── 06-Translate-Text/
│   ├── 07-Speech-Service/
│   └── 08-Speech-Translation/
├── 04-knowledge-mining/         # Cognitive Search implementations
│   ├── custom-skills/
│   ├── push-api/
│   └── vector-search/
├── 05-document-intelligence/    # Form processing and OCR
│   └── doc-intelligence/
├── 06-generative-ai/           # OpenAI and generative models
│   └── semantic-kernel/
├── 07-infrastructure/          # Infrastructure as Code
│   ├── 07-Bicep-Infrastructure/
│   ├── 09-Bicep-Loops/
│   └── 10-Bicep-Modules/
├── docs/                       # Additional documentation
├── templates/                  # Project templates
├── scripts/                    # Utility scripts
├── LEARNING_PROGRESS.md        # Detailed progress tracker
└── README.md                   # This file
```

## 📚 Completed Modules

### Natural Language Processing
- ✅ **Custom Entity Extraction** - Built custom NER model for classified ads
- ✅ **Text Translation** - Multi-language translation with 137 language support
- ✅ **Speech Service** - Speech-to-text and text-to-speech implementation
- ✅ **Speech Translation** - Real-time speech translation to multiple languages

### Knowledge Mining
- ✅ **Custom Skills** - Extended Azure Cognitive Search with custom skills
- ✅ **Push API** - Implemented document indexing via Push API
- ✅ **Vector Search** - Semantic search using embeddings

### Document Intelligence
- ✅ **Form Processing** - Extract structured data from documents

### Infrastructure as Code
- ✅ **Bicep Basics** - Parameterized Azure deployments
- ✅ **Bicep Loops** - Multi-region deployments with loops
- ✅ **Bicep Modules** - Reusable infrastructure components

## 🛠️ Technologies Used

- **Azure AI Services**: Language, Speech, Translation, Document Intelligence
- **Azure Infrastructure**: Bicep, ARM Templates, Resource Manager
- **Programming Languages**: Python 3.x, Bicep DSL
- **Development Tools**: VS Code, Azure CLI, Git

## 🎯 Learning Path

Following the official [Microsoft AI-102: Azure AI Engineer](https://learn.microsoft.com/en-us/certifications/azure-ai-engineer/) certification path.

## 📋 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/aihearticu/Azure-AI-Learning-Hub.git
   cd Azure-AI-Learning-Hub
   ```

2. **Environment Setup**
   - Copy `.env.example` to `.env` in each module
   - Add your Azure credentials
   - Install dependencies: `pip install -r requirements.txt`

3. **Azure Setup**
   - Create Azure subscription or use free trial
   - Set up required Azure services per module

## 🔗 Resources

- [Microsoft Learn - AI Engineer Path](https://learn.microsoft.com/en-us/training/paths/azure-ai-engineer/)
- [Azure AI Services Documentation](https://docs.microsoft.com/azure/cognitive-services/)
- [Azure Bicep Documentation](https://docs.microsoft.com/azure/azure-resource-manager/bicep/)

## 📝 Notes

Each module contains:
- Detailed README with implementation notes
- Working code examples
- Troubleshooting guides
- Configuration templates

---

*This repository serves as a comprehensive reference for Azure AI implementations and solutions to common challenges encountered during the certification journey.*