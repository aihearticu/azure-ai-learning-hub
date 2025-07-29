# Azure AI Learning Modules

This repository contains hands-on lab work completed while following the Microsoft Learn AI Language path.

## 📚 Completed Labs

### Lab 05: Extract Custom Entities
- **Status**: ✅ Completed (2025-07-28)
- **Technologies**: Azure AI Language, Custom NER
- **Key Learning**: Built custom entity recognition model to extract ItemForSale, Price, and Location from classified ads
- **Challenges Solved**: CORS configuration, storage account permissions

### Lab 06: Translate Text
- **Status**: ✅ Completed (2025-07-28)
- **Technologies**: Azure AI Translator
- **Key Learning**: Built interactive translation application supporting 137 languages with automatic source detection
- **Implementation**: Python SDK with real-time translation capabilities

### Lab 07: Bicep Infrastructure
- **Status**: ✅ Completed (2025-07-29)
- **Technologies**: Azure Bicep, Infrastructure as Code
- **Key Learning**: Built Bicep templates with parameters, variables, and modules for Azure resource deployment
- **Implementation**: Progressive exercises from basic resources to modular architecture

### Lab 07: Speech Service
- **Status**: ✅ Completed (2025-07-29)
- **Technologies**: Azure AI Speech Services, Python SDK
- **Key Learning**: Implemented speech-to-text and text-to-speech with real microphone support
- **Implementation**: Speaking clock app with both file-based and live audio capabilities
- **Special Achievement**: Successfully configured cross-platform audio (WSL files + Windows microphone)

### Lab 08: Speech Translation
- **Status**: ✅ Completed (2025-07-29)
- **Technologies**: Azure AI Speech Translation, Multi-language synthesis
- **Key Learning**: Real-time speech translation from English to French, Spanish, and Hindi
- **Implementation**: Translated "Where is the station?" with native voice synthesis for each language
- **Special Features**: Both file-based and microphone input with language-specific neural voices

### Lab 09: Bicep Conditions and Loops
- **Status**: ✅ Completed (2025-07-29)
- **Technologies**: Azure Bicep, Infrastructure as Code
- **Key Learning**: Conditional deployments and loop-based multi-region resource creation
- **Implementation**: 
  - Conditions: Deploy audit resources only in Production environments
  - Loops: Deploy SQL databases to multiple Azure regions using array parameters
- **Special Achievement**: Successfully deployed databases to West US and East US 2 regions

## 🚀 Repository Structure

```
Azure-AI-Learning-Modules/
├── 05-Custom-Entity-Extraction/
│   ├── README.md
│   ├── TROUBLESHOOTING.md
│   └── src/                    # Implementation files
├── 06-Translate-Text/
│   ├── README.md
│   └── src/                    # Translation app
├── 07-Bicep-Infrastructure/
│   ├── README.md
│   ├── src/                    # Bicep templates
│   │   ├── main.bicep          # Basic version
│   │   ├── main-with-params.bicep  # Parameterized
│   │   ├── main-modular.bicep  # With modules
│   │   └── modules/            # Reusable modules
│   ├── exercises/              # Progressive exercises
│   ├── deployments/            # Deployment scripts
│   └── docs/                   # Documentation
├── 07-Speech-Service/
│   ├── README.md
│   ├── TROUBLESHOOTING.md      # Common issues and solutions
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example           # Template for credentials
│   ├── src/
│   │   ├── speaking-clock.py   # File-based version
│   │   ├── speaking-clock-mic.py # Microphone version
│   │   ├── time.wav           # Sample input audio
│   │   └── output.wav         # Generated speech
│   └── venv/                  # Python virtual environment
├── 08-Speech-Translation/
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example
│   ├── src/
│   │   ├── station.wav        # "Where is the station?"
│   │   ├── translator.py      # Interactive translator
│   │   ├── simple-translator.py # Automated demo
│   │   ├── translator-mic.py  # Microphone version
│   │   └── translated_*.wav   # Generated translations
│   └── venv/                  # Python virtual environment
├── 09-Bicep-Loops/
│   ├── README.md
│   └── (Bicep files in parent directory)
├── memory/                      # Learning progress tracking
└── README.md                    # This file
```

## 🛠️ Technologies Used

- **Azure AI Services**
  - Azure AI Language
  - Azure AI Translator
- **Azure Infrastructure**
  - Azure Bicep (Infrastructure as Code)
  - Azure Resource Manager
- **Programming Languages**
  - Python 3.x
  - Bicep DSL
- **SDKs**
  - azure-ai-textanalytics
  - azure-ai-translation-text
  - Azure CLI

## 📋 Upcoming Labs

- [ ] 01 - Get Started with Azure AI Services
- [ ] 02 - Analyze Text
- [ ] 03 - Question Answering
- [ ] 04 - Text Classification
- [ ] 07 - Speech Services
- [ ] 08 - Speech Translation
- [ ] 09 - Conversational AI

## 🔗 Resources

- [Microsoft Learn - AI Language](https://microsoftlearning.github.io/mslearn-ai-language/)
- [Azure AI Services Documentation](https://docs.microsoft.com/azure/cognitive-services/)

## 📝 Notes

Each lab folder contains:
- Detailed README with implementation notes
- Source code with working examples
- Troubleshooting guides for common issues
- .env.example files for configuration reference

---

*This repository serves as a reference for Azure AI implementations and solutions to common challenges encountered during the learning process.*