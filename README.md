# 🚀 Azure AI Learning Hub

![Azure AI Services](https://img.shields.io/badge/Azure-AI%20Services-0078D4?style=for-the-badge&logo=microsoft-azure)
![Labs](https://img.shields.io/badge/Labs-130%2B-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=for-the-badge)

> A comprehensive learning repository for mastering Azure AI Services with 130+ hands-on labs, practical examples, and real-world implementations.

## 🎯 Overview

This repository serves as a complete learning hub for Azure AI Services, covering everything from fundamentals to advanced implementations. Whether you're preparing for the AI-102 certification or building production-ready AI solutions, you'll find structured learning paths, hands-on labs, and best practices.

## 📚 Learning Paths

### 1. [AI Fundamentals](./01-fundamentals/)
- Azure AI Services Overview
- Security & Responsible AI
- Container Deployment
- Cost Management

### 2. [Computer Vision](./02-computer-vision/)
- Image Analysis & Classification
- Optical Character Recognition (OCR)
- Face Detection & Recognition
- Video Analysis & Indexing

### 3. [Natural Language Processing](./03-natural-language/)
- Text Analytics & Sentiment Analysis
- Question Answering Systems
- Language Translation
- Speech Services (STT/TTS)

### 4. [Knowledge Mining](./04-knowledge-mining/)
- Azure Cognitive Search
- Vector Search Implementation
- Custom Skills Development
- Semantic Search

### 5. [Document Intelligence](./05-document-intelligence/)
- Form Recognition
- Custom Model Training
- Invoice & Receipt Processing
- Contract Analysis

### 6. [Generative AI](./06-generative-ai/)
- Azure OpenAI Integration
- GPT Model Implementation
- DALL-E Image Generation
- Embeddings & RAG Systems

## 🚀 Quick Start

### Prerequisites
- Azure subscription ([free account](https://azure.microsoft.com/free/))
- Python 3.8+ or .NET 6.0+
- Azure CLI installed
- Git for version control

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/AIHeartICU/azure-ai-learning-hub.git
   cd azure-ai-learning-hub
   ```

2. **Set up your environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install base requirements
   pip install -r requirements.txt
   ```

3. **Configure Azure credentials**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your Azure credentials
   # NEVER commit your actual credentials!
   ```

4. **Choose your learning path**
   - Browse the learning paths above
   - Each path contains multiple labs with step-by-step instructions
   - Start with fundamentals if you're new to Azure AI

## 📂 Repository Structure

```
azure-ai-learning-hub/
├── 01-fundamentals/         # Core concepts and setup
├── 02-computer-vision/      # Vision services labs
├── 03-natural-language/     # Language services labs
├── 04-knowledge-mining/     # Search and mining labs
├── 05-document-intelligence/# Document processing labs
├── 06-generative-ai/       # Azure OpenAI labs
├── templates/              # Reusable templates
├── scripts/                # Utility scripts
└── resources/              # Sample data and assets
```

## 🔧 Key Features

### 📊 Comprehensive Labs
- **130+ hands-on labs** covering all Azure AI services
- Step-by-step instructions with screenshots
- Multiple programming language support (Python, C#, JavaScript)
- Real-world scenarios and use cases

### 🛡️ Best Practices
- Security-first approach
- Cost optimization strategies
- Performance tuning guides
- Production deployment patterns

### 🤝 Community Driven
- Regular updates with new services
- Community contributions welcome
- Discussion forums for Q&A
- Code review and feedback

### 🎓 Certification Aligned
- Covers AI-102 exam objectives
- Practice exercises and quizzes
- Study guides and cheat sheets
- Mock exam questions

## 💻 Sample Projects

### Completed Labs
1. **[Question Answering System](./azure-ai-question-answering-lab/)** - Build a custom Q&A bot using Language Service
2. **Image Classification API** - Computer Vision for product categorization
3. **Document Data Extractor** - Form Recognizer for invoice processing
4. **Multilingual Chat Bot** - Translation and Language Understanding
5. **Video Content Analyzer** - Video Indexer for media insights

### Coming Soon
- Semantic Search Engine
- AI-Powered Content Moderator
- Custom Vision Model Builder
- Speech-to-Speech Translator
- RAG Implementation with GPT-4

## 📈 Progress Tracking

Track your learning progress:
- [ ] Complete Fundamentals Path
- [ ] Build 5 Computer Vision Projects
- [ ] Implement 3 NLP Solutions
- [ ] Deploy 1 Production System
- [ ] Pass AI-102 Certification

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:
- Code standards
- Lab template format
- Pull request process
- Issue reporting

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Resources

### Official Documentation
- [Azure AI Services Docs](https://docs.microsoft.com/azure/cognitive-services/)
- [Azure AI Blog](https://azure.microsoft.com/blog/topics/ai/)
- [Microsoft Learn](https://learn.microsoft.com/training/azure/)

### Community
- [GitHub Discussions](https://github.com/AIHeartICU/azure-ai-learning-hub/discussions)
- [Azure AI Community](https://techcommunity.microsoft.com/t5/ai-cognitive-services/bd-p/CognitiveServices)
- [Stack Overflow - Azure AI](https://stackoverflow.com/questions/tagged/azure-cognitive-services)

### Tools & Extensions
- [Azure AI CLI](https://docs.microsoft.com/azure/cognitive-services/cognitive-services-cli)
- [VS Code Azure Extensions](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
- [Postman Collection](./resources/postman/)

## 📊 Stats

- **Total Labs**: 130+
- **Services Covered**: 15+
- **Code Samples**: 500+
- **Contributors**: Growing community
- **Last Updated**: January 2025

---

<p align="center">
  <strong>🌟 Star this repository to bookmark it for future reference!</strong>
</p>

<p align="center">
  Made with ❤️ by the Azure AI Learning Community
</p>