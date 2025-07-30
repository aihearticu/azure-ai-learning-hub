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
pip install flask requests python-dotenv pylint matplotlib pillow

# Numpy (specific upgrade needed)
pip install --upgrade numpy

# Azure AI packages
pip install azure-ai-textanalytics azure-cognitiveservices-speech azure-ai-vision-imageanalysis
pip install azure-ai-formrecognizer azure-cognitiveservices-language-luis
pip install openai azure-identity azure-ai-ml

# Jupyter for notebooks
pip install jupyter ipykernel
python -m ipykernel install --user --name=azureai
```

### Environment Variables Setup
```bash
# Create .env file in project root
cat > .env << EOL
# Azure Cognitive Services
AZURE_COGNITIVE_SERVICES_KEY=your_key_here
AZURE_COGNITIVE_SERVICES_ENDPOINT=https://your-resource.cognitiveservices.azure.com/

# Azure OpenAI
AZURE_OPENAI_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment

# Other services as needed
EOL
```

## 🔧 VS Code Configuration

### Required Extensions
```bash
# Install via command line
code --install-extension ms-python.python
code --install-extension ms-dotnettools.csharp
code --install-extension ms-azuretools.vscode-azurefunctions
code --install-extension ms-vscode.PowerShell
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-toolsai.jupyter
```

### Recommended Settings
```json
{
  "python.defaultInterpreterPath": "~/miniconda3/envs/azureai/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "files.autoSave": "afterDelay",
  "terminal.integrated.defaultProfile.linux": "bash"
}
```

## 🚨 Common Setup Issues & Solutions

### Issue 1: Python Package Conflicts
```bash
# Solution: Use virtual environments
conda create -n lab_specific python=3.11 -y
conda activate lab_specific
pip install -r requirements.txt
```

### Issue 2: Azure CLI Authentication
```bash
# Clear cached credentials
az account clear
az login --use-device-code  # For headless environments
```

### Issue 3: Node.js Version Conflicts
```bash
# Use nvm for version management
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
nvm use --lts
```

### Issue 4: PATH Variables (Windows)
```powershell
# Add to system PATH
[Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\tools\miniconda3\Scripts", "User")
```

## 📋 Pre-Lab Checklist

Before starting any lab, verify:

```bash
# 1. Azure CLI logged in
az account show

# 2. Python environment activated
conda activate azureai
python --version

# 3. Node/npm available
node --version
npm --version

# 4. .NET SDK ready
dotnet --version

# 5. Git configured
git config --global user.name
git config --global user.email

# 6. VS Code extensions
code --list-extensions | grep -E "(python|azure|csharp)"
```

## 🛡️ Best Practices for Reliability

### 1. Environment Isolation
- Use separate conda environments per project
- Pin package versions in requirements.txt
- Document exact versions that work

### 2. Cost Management
```bash
# Set spending limits
az consumption budget create \
  --amount 50 \
  --budget-name "AI-Learning-Budget" \
  --category cost \
  --time-grain Monthly

# Use free tiers when possible
az cognitiveservices account create \
  --name "myservice" \
  --resource-group "rg-learning" \
  --kind "TextAnalytics" \
  --sku "F0" \  # Free tier
  --location "eastus"
```

### 3. Resource Cleanup
```bash
# Delete resource groups after labs
az group delete --name "lab-rg" --yes --no-wait

# List all your resource groups
az group list --output table
```

### 4. Version Control Everything
```bash
# Standard .gitignore for AI projects
cat > .gitignore << EOL
.env
*.key
.azure/
__pycache__/
*.pyc
.DS_Store
node_modules/
.vscode/settings.json
EOL
```

## 🔄 Quick Setup Script

Save this as `setup-azure-ai-env.sh`:

```bash
#!/bin/bash

echo "🚀 Setting up Azure AI Development Environment"

# Check prerequisites
command -v git >/dev/null 2>&1 || { echo "Git required but not installed."; exit 1; }
command -v conda >/dev/null 2>&1 || { echo "Conda required but not installed."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js required but not installed."; exit 1; }
command -v dotnet >/dev/null 2>&1 || { echo ".NET SDK required but not installed."; exit 1; }

# Create conda environment
echo "📦 Creating Python environment..."
conda create -n azureai python=3.11 -y
conda activate azureai

# Install Python packages
echo "🐍 Installing Python packages..."
pip install flask requests python-dotenv pylint matplotlib pillow
pip install --upgrade numpy
pip install azure-ai-textanalytics azure-cognitiveservices-speech openai

# Install Node packages
echo "📦 Installing Node.js packages..."
npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Setup VS Code
echo "🔧 Configuring VS Code..."
code --install-extension ms-python.python
code --install-extension ms-azuretools.vscode-azurefunctions

# Azure CLI login
echo "☁️ Logging into Azure..."
az login

echo "✅ Setup complete! Run 'conda activate azureai' to start."
```

## 📚 Additional Resources

- [Azure AI Services Documentation](https://docs.microsoft.com/azure/cognitive-services/)
- [Python SDK Samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/cognitiveservices)
- [Cost Management Best Practices](https://docs.microsoft.com/azure/cost-management-billing/)
- [VS Code Azure Extensions](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

---

*This setup guide ensures consistent, reliable development environment across all Azure AI learning modules.*