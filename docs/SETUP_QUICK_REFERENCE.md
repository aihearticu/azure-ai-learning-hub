# Azure AI Setup Quick Reference Card 🚀

## Essential Commands - Copy & Paste Ready

### 🔧 Initial Setup (One Time)
```bash
# 1. Check prerequisites
git --version          # Need 2.30+
python --version       # Need 3.11
node --version         # Need 18.x or 20.x
dotnet --version       # Need 8.0
az --version           # Need 2.50+

# 2. Create Python environment
conda create -n azureai python=3.11 -y
conda activate azureai

# 3. Install all packages at once
pip install flask requests python-dotenv pylint matplotlib pillow \
    azure-ai-textanalytics azure-cognitiveservices-speech \
    azure-ai-vision-imageanalysis azure-ai-formrecognizer \
    openai azure-identity azure-ai-ml jupyter ipykernel \
    --upgrade numpy

# 4. VS Code extensions
code --install-extension ms-python.python ms-dotnettools.csharp \
    ms-azuretools.vscode-azurefunctions ms-vscode.PowerShell
```

### 🏁 Before Each Lab
```bash
# 1. Activate environment
conda activate azureai

# 2. Login to Azure
az login
az account show

# 3. Set default subscription (if multiple)
az account set --subscription "Your Subscription Name"

# 4. Create resource group for lab
az group create --name "rg-lab-$(date +%Y%m%d)" --location eastus
```

### 🧹 After Each Lab
```bash
# List your resource groups
az group list --output table

# Delete lab resources
az group delete --name "rg-lab-YYYYMMDD" --yes --no-wait

# Clear Azure CLI cache if needed
az cache purge
az account clear
```

### 💰 Cost Control Commands
```bash
# Use FREE tiers
az cognitiveservices account create \
  --name "free-text-analytics" \
  --resource-group "rg-learning" \
  --kind "TextAnalytics" \
  --sku "F0" \
  --location "eastus"

# Check current usage
az consumption usage list \
  --start-date "2025-07-01" \
  --end-date "2025-07-31" \
  --output table
```

### 🐛 Common Fixes
```bash
# Python package conflicts
pip uninstall -y <package> && pip install <package>

# Node version issues
nvm use 20

# Azure CLI issues
az logout && az login --use-device-code

# Clear all Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

### 📁 Project Structure Template
```bash
mkdir new-lab && cd new-lab
cat > .env << 'EOF'
AZURE_KEY=your-key
AZURE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
EOF

echo ".env" > .gitignore
echo "__pycache__/" >> .gitignore
```

### 🔑 Environment Variables
```bash
# Load .env file in Python
from dotenv import load_dotenv
import os
load_dotenv()
key = os.getenv("AZURE_KEY")

# Load .env in Node.js
require('dotenv').config();
const key = process.env.AZURE_KEY;

# Load in .NET
var config = new ConfigurationBuilder()
    .AddEnvironmentVariables()
    .AddUserSecrets<Program>()
    .Build();
```

## 🎯 Lab-Specific Setups

### Vision Labs
```bash
pip install azure-ai-vision-imageanalysis opencv-python
```

### Language Labs
```bash
pip install azure-ai-textanalytics transformers
```

### Speech Labs
```bash
pip install azure-cognitiveservices-speech pyaudio
```

### Search Labs
```bash
pip install azure-search-documents
npm install @azure/search-documents
```

### OpenAI Labs
```bash
pip install openai tiktoken
```

---
*Keep this handy during all Azure AI labs!*