# Azure AI Services Development Environment Setup Guide

## Overview
This guide ensures a reliable, consistent setup for Azure AI services development across all 130+ learning modules.

## 🖥️ Operating System Recommendations

### Primary Recommendation: Windows 11
- Best compatibility with all Azure tools
- Native support for all SDKs
- Consistent with Microsoft lab environments

### Alternative Options
- **Linux (Ubuntu 20.04+)**: Good support, may need adaptations
- **macOS**: Supported, some tools may require Homebrew
- **WSL2 on Windows**: Best of both worlds for Linux users

## 📦 Required Software Stack

### 1. Core Development Tools

```bash
# Web Browser
- Microsoft Edge (recommended) or Chrome

# Version Control
git --version  # Should be 2.30+

# Code Editor
- Visual Studio Code (latest stable)
```

### 2. Language Runtimes

#### .NET Core SDK 8.0
```bash
# Download from: https://dotnet.microsoft.com/download
dotnet --version  # Should show 8.0.x

# Verify installation
dotnet new console -o test
cd test && dotnet run
```

#### Node.js (Latest LTS)
```bash
# Download from: https://nodejs.org/
node --version  # Should be 18.x or 20.x
npm --version   # Should be 9.x+

# Verify
npm init -y && npm install axios
```

#### Python 3.11 (via Miniconda)
```bash
# Download from: https://docs.conda.io/en/latest/miniconda.html
conda --version
python --version  # Should be 3.11.x

# Create AI services environment
conda create -n azureai python=3.11 -y
conda activate azureai
```

### 3. Azure Tools

#### Azure CLI
```bash
# Installation
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash  # Linux
brew install azure-cli  # macOS
# Windows: Download MSI from Azure website

# Verify and login
az --version  # Should be 2.50+
az login
az account show
```

#### Azure Functions Core Tools
```bash
npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Verify
func --version
```

### 4. Visual C++ Redistributable (Windows Only)
- Required for some Python packages
- Download from Microsoft: Latest Visual C++ Redistributable

## 🐍 Python Environment Setup

### Essential AI Services Packages
```bash
# Activate your conda environment first
conda activate azureai

# Core packages
pip install python-dotenv
pip install requests

# Azure AI Services SDKs
pip install azure-ai-textanalytics
pip install azure-cognitiveservices-vision-computervision
pip install azure-cognitiveservices-speech
pip install azure-ai-formrecognizer
pip install azure-search-documents
pip install azure-ai-translation-text
pip install azure-ai-language-questionanswering
pip install azure-ai-language-conversations

# OpenAI Integration
pip install openai
pip install tiktoken

# Utilities
pip install numpy pandas matplotlib
pip install jupyter notebook ipykernel
```

## 🔐 Azure Subscription Setup

### 1. Create Free Azure Account
- Navigate to [azure.microsoft.com/free](https://azure.microsoft.com/free)
- Sign up with Microsoft account
- Get $200 credit for 30 days
- Many AI services have free tiers

### 2. Set Up Resource Groups
```bash
# Standard naming convention
az group create --name rg-ai-learning --location eastus
```

### 3. Create AI Services Multi-Service Resource
```bash
az cognitiveservices account create \
    --name ai-learning-services \
    --resource-group rg-ai-learning \
    --kind CognitiveServices \
    --sku S0 \
    --location eastus \
    --yes
```

## 🛠️ VS Code Extensions

### Required Extensions
```
# Install via VS Code Extensions panel or command line
code --install-extension ms-python.python
code --install-extension ms-azuretools.vscode-azurefunctions
code --install-extension ms-vscode.azure-account
code --install-extension ms-dotnettools.csharp
code --install-extension ms-toolsai.jupyter
code --install-extension ms-azure-devops.azure-pipelines
```

## 📁 Project Structure Template

```
azure-ai-project/
├── .env.example          # Template for environment variables
├── .gitignore           # Ignore credentials and temp files
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
├── src/                # Source code
│   ├── __init__.py
│   └── main.py
├── tests/              # Test files
│   └── test_main.py
└── notebooks/          # Jupyter notebooks
    └── exploration.ipynb
```

## 🔧 Environment Variables Template

Create `.env` file:
```bash
# Azure AI Services
AZURE_AI_SERVICES_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_AI_SERVICES_KEY=your-key-here

# Specific Services (if using individual resources)
AZURE_LANGUAGE_ENDPOINT=https://your-language.cognitiveservices.azure.com/
AZURE_LANGUAGE_KEY=your-key-here

AZURE_VISION_ENDPOINT=https://your-vision.cognitiveservices.azure.com/
AZURE_VISION_KEY=your-key-here

# OpenAI
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_OPENAI_KEY=your-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment

# Search
AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_SEARCH_KEY=your-key-here
```

## ✅ Verification Checklist

Run these commands to verify your setup:

```bash
# Check versions
python --version          # 3.11.x
node --version           # 18.x or 20.x
dotnet --version         # 8.0.x
az --version            # 2.50+
func --version          # 4.x
git --version           # 2.30+

# Test Azure connection
az account show

# Test Python packages
python -c "import azure.ai.textanalytics; print('Azure SDK installed')"

# Test .NET
dotnet new console -n test && cd test && dotnet run && cd .. && rm -rf test
```

## 🚨 Common Issues & Solutions

### Issue: SSL Certificate Errors
```bash
# Solution for Python
pip config set global.trusted-host "pypi.org files.pythonhosted.org"
```

### Issue: Azure CLI Login Problems
```bash
# Clear cached credentials
az account clear
az login --use-device-code
```

### Issue: Python Package Installation Fails
```bash
# Use conda-forge channel
conda install -c conda-forge [package-name]
```

## 📚 Additional Resources

- [Azure AI Services Documentation](https://docs.microsoft.com/azure/cognitive-services/)
- [Python SDK Samples](https://github.com/Azure/azure-sdk-for-python)
- [.NET SDK Samples](https://github.com/Azure/azure-sdk-for-net)
- [Azure AI Learning Path](https://learn.microsoft.com/training/paths/azure-ai-fundamentals/)

---
*Keep this guide handy throughout your Azure AI learning journey!*