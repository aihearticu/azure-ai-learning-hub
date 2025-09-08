# Azure AI Services Container Lab

A comprehensive testing suite for Azure AI Services running in containers, demonstrating Language Detection, Sentiment Analysis, Key Phrase Extraction, and Named Entity Recognition.

## 🎯 Learning Objectives

By completing this lab, you will:
- Deploy Azure AI Services in Docker containers
- Understand the benefits of containerized AI services
- Test all major text analytics capabilities
- Monitor container performance and health
- Compare container vs cloud service performance
- Implement PII detection and redaction

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│     Your Application/Tests          │
│  (Python scripts, REST API calls)   │
└──────────────┬──────────────────────┘
               │ HTTP/REST
               ▼
┌─────────────────────────────────────┐
│   Docker Container (Local)          │
│  Azure AI Language Service Image    │
│   - Language Detection              │
│   - Sentiment Analysis              │
│   - Key Phrase Extraction          │
│   - Entity Recognition              │
│   - PII Detection                   │
└──────────────┬──────────────────────┘
               │ Billing/Telemetry
               ▼
┌─────────────────────────────────────┐
│   Azure Cognitive Services          │
│        (Cloud - Billing)            │
└─────────────────────────────────────┘
```

## 📋 Prerequisites

1. **Azure Subscription** with Cognitive Services access
2. **Docker** installed and running
3. **Python 3.8+** installed
4. **Azure CLI** (optional but recommended)
5. **Container access** (Request at https://aka.ms/csgate)

## 🚀 Quick Start

### 1. Initial Setup
```bash
# Clone or navigate to the lab directory
cd Azure-AI-Learning-Modules/container-lab

# Run the setup script
chmod +x setup.sh
./setup.sh

# Install dependencies
pip3 install -r requirements.txt
```

### 2. Configure Credentials
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Azure credentials
nano .env  # or use your preferred editor
```

### 3. Deploy Container
```bash
# Deploy the Azure AI Services container
./scripts/deploy-container.sh
```

### 4. Run Tests
```bash
# Run all tests
./scripts/run-all-tests.sh

# Or run individual tests:
python3 scripts/test-language-detection.py
python3 scripts/test-sentiment-analysis.py
python3 scripts/test-key-phrases.py
python3 scripts/test-entity-recognition.py
```

### 5. Monitor Container
```bash
# Real-time monitoring
./scripts/monitor-container.sh
```

## 📁 Project Structure

```
container-lab/
├── .env.example           # Environment template
├── .env                   # Your credentials (gitignored)
├── requirements.txt       # Python dependencies
├── setup.sh              # Initial setup script
├── README.md             # This file
├── scripts/
│   ├── deploy-container.sh        # Container deployment
│   ├── run-all-tests.sh          # Run all tests
│   ├── monitor-container.sh       # Performance monitoring
│   ├── test-language-detection.py # Language detection tests
│   ├── test-sentiment-analysis.py # Sentiment analysis tests
│   ├── test-key-phrases.py       # Key phrase extraction
│   └── test-entity-recognition.py # Entity & PII recognition
├── data/                 # Test data files
├── docs/                 # Additional documentation
└── tests/                # Additional test scenarios
```

## 🔬 Test Scenarios

### Language Detection
- Multi-language text samples
- Confidence scoring
- Performance comparison (container vs cloud)

### Sentiment Analysis
- Positive, negative, and mixed sentiments
- Sentence-level analysis
- Opinion mining with aspects and assessments

### Key Phrase Extraction
- Domain-specific terminology extraction
- Importance ranking
- Word frequency visualization

### Entity Recognition
- Person, Organization, Location entities
- DateTime, Quantity, Product recognition
- PII detection and redaction
- Wikipedia entity linking

## 📊 Container Benefits

| Feature | Container | Cloud Service |
|---------|-----------|---------------|
| **Latency** | Ultra-low (local) | Network dependent |
| **Data Privacy** | Data stays local | Data sent to cloud |
| **Offline Capability** | Yes | No |
| **Scalability** | Limited by hardware | Unlimited |
| **Cost Model** | Fixed + minimal usage | Pay per API call |
| **Compliance** | Full control | Shared responsibility |

## 🛠️ Troubleshooting

### Container won't start
```bash
# Check Docker status
docker ps -a

# View container logs
docker logs azure-ai-language

# Verify credentials
echo $AZURE_COGNITIVE_SERVICES_KEY
```

### API calls failing
```bash
# Test container health
curl http://localhost:5000/health

# Check firewall/ports
sudo netstat -tlnp | grep 5000
```

### Performance issues
```bash
# Check resource usage
docker stats azure-ai-language

# Allocate more resources
docker update --memory="4g" --cpus="2" azure-ai-language
```

## 📈 Performance Tuning

### Container Resources
```bash
# Run with specific resources
docker run -d \
  --name azure-ai-language \
  --memory="4g" \
  --cpus="2" \
  -p 5000:5000 \
  -e Eula=accept \
  -e Billing=$ENDPOINT \
  -e ApiKey=$KEY \
  mcr.microsoft.com/azure-cognitive-services/textanalytics/language
```

### Batch Processing
- Process multiple documents in single requests
- Use async processing for large volumes
- Implement connection pooling

## 🔐 Security Best Practices

1. **Never commit credentials** - Use .env files and .gitignore
2. **Use Azure Key Vault** for production
3. **Implement rate limiting** in your application
4. **Enable container security scanning**
5. **Use private endpoints** in production
6. **Regular security updates** for base images

## 📚 Additional Resources

- [Azure AI Services Documentation](https://docs.microsoft.com/azure/cognitive-services/)
- [Container Documentation](https://docs.microsoft.com/azure/cognitive-services/containers/)
- [Language Service API Reference](https://docs.microsoft.com/rest/api/language/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Request Container Access](https://aka.ms/csgate)

## 🎓 Learning Exercises

### Exercise 1: Multi-language Support
Modify the language detection test to include more languages and analyze the confidence scores.

### Exercise 2: Custom Sentiment Thresholds
Create custom logic to categorize sentiment based on confidence thresholds.

### Exercise 3: Entity Extraction Pipeline
Build a pipeline that extracts entities and generates a knowledge graph.

### Exercise 4: PII Redaction Service
Create a service that automatically redacts PII from uploaded documents.

### Exercise 5: Performance Benchmarking
Compare response times between container and cloud across different payload sizes.

## 📝 Notes

- Container images require billing endpoint connection
- Some features may have different versions in containers vs cloud
- Containers are ideal for edge deployments and regulated industries
- Regular updates ensure latest model versions

## 🤝 Contributing

Feel free to add more test scenarios or improve existing scripts!

---

**Created for**: Azure AI Engineer Learning Path  
**Last Updated**: 2024  
**Author**: AI Learning Lab