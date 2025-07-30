# AI-102 Priority Learning Plan

## 📊 Current Exam Coverage Analysis

Based on your completed labs and AI-102 exam weights:

| Exam Area | Weight | Your Coverage | Priority |
|-----------|--------|---------------|----------|
| Plan & Manage Azure AI | 15-20% | 🟡 Partial (containers only) | Medium |
| Computer Vision | 15-20% | ❌ 0% | **HIGH** |
| Natural Language | 15-20% | ❌ 0% | **HIGH** |
| Knowledge Mining | 15-20% | 🟢 Good (3 labs) | Low |
| Generative AI | 10-15% | ❌ 0% | **HIGH** |
| Agentic Solutions | 10-15% | ❌ 0% | Medium |

## 🎯 Recommended Learning Order

### Phase 1: Fill Major Gaps (Next 2-3 weeks)
**Goal**: Cover 0% areas that represent 40-50% of exam

#### Week 1: Computer Vision Sprint
1. **Image Analysis with Computer Vision**
   - Analyze images
   - Generate thumbnails
   - Detect objects and brands
   
2. **Custom Vision**
   - Classification models
   - Object detection models
   
3. **Face API**
   - Face detection
   - Face verification

#### Week 2: Natural Language Sprint
1. **Text Analytics**
   - Sentiment analysis
   - Key phrase extraction
   - Named entity recognition
   
2. **Language Understanding**
   - Intent recognition
   - Entity extraction
   
3. **Translation & QnA**
   - Translator service
   - Question answering

#### Week 3: Generative AI Sprint
1. **Azure OpenAI Basics**
   - GPT models setup
   - Completions API
   
2. **Prompt Engineering**
   - Few-shot learning
   - Chain of thought
   
3. **Responsible AI**
   - Content filtering
   - Bias mitigation

### Phase 2: Strengthen Foundations (Week 4)
1. **Complete AI Services Fundamentals**
   - Security configurations
   - Monitoring and logging
   - Cost optimization

2. **Agentic Solutions Introduction**
   - Bot Framework basics
   - Conversational design

### Phase 3: Advanced Integration (Week 5-6)
1. **Cross-Service Integration**
   - Combine vision + language
   - Search + OpenAI
   
2. **Production Deployment**
   - CI/CD pipelines
   - Edge deployment

## 📈 Quick Win Strategy

### This Week's Focus: Computer Vision
Start with Computer Vision because:
- 15-20% of exam (high weight)
- Many prebuilt models (quick wins)
- Visual results (satisfying progress)

### Suggested Lab Order:
1. **Today**: Image Analysis basics
2. **Tomorrow**: Custom Vision classifier
3. **Day 3**: OCR and Read API
4. **Day 4**: Face detection
5. **Day 5**: Video Analyzer

## 🔧 Lab Setup Tips

### For Computer Vision:
```bash
# Clone the repo
git clone https://github.com/MicrosoftLearning/mslearn-ai-vision.git

# Create resource
az cognitiveservices account create \
  --name "vision-$(date +%Y%m%d)" \
  --resource-group "rg-ai-learning" \
  --kind "ComputerVision" \
  --sku "F0" \
  --location "eastus"
```

### For Natural Language:
```bash
# Clone the repo
git clone https://github.com/MicrosoftLearning/mslearn-ai-language.git

# Create multi-service resource
az cognitiveservices account create \
  --name "language-$(date +%Y%m%d)" \
  --resource-group "rg-ai-learning" \
  --kind "CognitiveServices" \
  --sku "S0" \
  --location "eastus"
```

### For Azure OpenAI:
```bash
# Note: Requires application approval
# Apply at: https://aka.ms/oai/access
```

## 📅 6-Week Certification Timeline

| Week | Focus Area | Target Labs | Exam Coverage |
|------|------------|-------------|---------------|
| 1 | Computer Vision | 5 labs | +15-20% |
| 2 | Natural Language | 5 labs | +15-20% |
| 3 | Generative AI | 4 labs | +10-15% |
| 4 | Fundamentals + Agentic | 4 labs | +10-15% |
| 5 | Integration + Practice | 3 labs | Reinforcement |
| 6 | Review + Practice Exam | - | Final prep |

## ✅ Success Metrics

Track your progress:
- [ ] Complete 1 lab per day minimum
- [ ] Document each lab in learning hub
- [ ] Take practice assessment after each area
- [ ] Build 1 integrated project combining services

## 🎓 Exam Readiness Checklist

Before scheduling AI-102:
- [ ] 80%+ on practice assessments
- [ ] Completed all priority areas
- [ ] Built 2+ integrated solutions
- [ ] Can explain all services to others
- [ ] Comfortable with SDK and REST APIs

---
*Your current 10% coverage needs to reach 80%+ for exam confidence*