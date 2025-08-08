# 📚 AI-102 Azure AI Engineer Associate - Complete Exam Study Guide

## 🎯 Exam Overview
- **Exam Code**: AI-102
- **Title**: Designing and Implementing a Microsoft Azure AI Solution
- **Duration**: 100 minutes
- **Questions**: 40-60 questions
- **Passing Score**: 700/1000
- **Cost**: $165 USD
- **Languages**: English, Japanese, Chinese (Simplified), Korean, German, French, Spanish, Portuguese (Brazil), Arabic (Saudi Arabia), Russian, Chinese (Traditional), Italian

---

## 📊 Exam Skill Domains (Updated 2024)

### Domain Distribution
1. **Plan and manage an Azure AI solution** (25-30%)
2. **Implement computer vision solutions** (20-25%)
3. **Implement natural language processing solutions** (20-25%)
4. **Implement knowledge mining and document intelligence solutions** (15-20%)
5. **Implement generative AI solutions** (15-20%)

---

# Domain 1: Plan and Manage an Azure AI Solution (25-30%)

## Select the appropriate Azure AI service

### Key Concepts to Master
```
Computer Vision → Image analysis, OCR, spatial analysis
Custom Vision → Custom image classification and object detection
Face → Face detection, verification, identification
Form Recognizer → Document data extraction
Video Indexer → Video insights and analysis

Language Service → Text analytics, NER, sentiment
Translator → Text and document translation
Speech → STT, TTS, translation, speaker recognition
CLU → Conversational language understanding

OpenAI Service → GPT, DALL-E, Embeddings
Content Moderator → Text and image moderation
Cognitive Search → Knowledge mining, vector search
```

### Decision Matrix
| Scenario | Service | Why |
|----------|---------|-----|
| Extract text from images | Computer Vision Read API | Handles printed and handwritten text |
| Custom product detection | Custom Vision | Train with your own images |
| Multi-language chatbot | CLU + Translator | Intent recognition + translation |
| Document processing | Form Recognizer | Structured data extraction |
| Semantic search | Cognitive Search + OpenAI | Vector embeddings for similarity |
| Real-time transcription | Speech Service | Streaming STT capabilities |
| Content filtering | Content Moderator | Built-in moderation models |

### ⚠️ Exam Tips
- Know the differences between Computer Vision and Custom Vision
- Understand when to use Form Recognizer vs OCR
- Remember Language Service consolidated multiple services
- Know the limits of each pricing tier

## Plan and configure security for Azure AI services

### Security Checklist
```python
# 1. Authentication Methods
- Subscription keys (avoid in production)
- Azure AD authentication (recommended)
- Managed identities (best practice)

# 2. Network Security
- Private endpoints
- Virtual networks
- Service firewalls
- IP restrictions

# 3. Data Protection
- Encryption at rest (automatic)
- Encryption in transit (TLS 1.2)
- Customer-managed keys (CMK)
- Data residency requirements

# 4. Access Control
- RBAC roles:
  - Cognitive Services Contributor
  - Cognitive Services User
  - Cognitive Services Data Reader
  - Custom roles

# 5. Compliance
- GDPR, HIPAA, SOC 2
- Data retention policies
- Audit logging
- PII handling
```

### Implementation Examples
```python
# Managed Identity Authentication
from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient

credential = DefaultAzureCredential()
client = TextAnalyticsClient(
    endpoint="https://myservice.cognitiveservices.azure.com/",
    credential=credential
)

# Key Vault Integration
from azure.keyvault.secrets import SecretClient

secret_client = SecretClient(
    vault_url="https://myvault.vault.azure.net/",
    credential=DefaultAzureCredential()
)
api_key = secret_client.get_secret("cognitive-services-key").value

# Private Endpoint Configuration (ARM template)
{
  "type": "Microsoft.Network/privateEndpoints",
  "properties": {
    "privateLinkServiceConnections": [{
      "properties": {
        "privateLinkServiceId": "[resourceId('Microsoft.CognitiveServices/accounts', 'myaccount')]",
        "groupIds": ["account"]
      }
    }]
  }
}
```

## Create and manage Azure AI service resources

### Deployment Options
1. **Azure Portal**: GUI-based, good for exploration
2. **Azure CLI**: Scriptable, good for automation
3. **PowerShell**: Windows-centric automation
4. **ARM/Bicep Templates**: Infrastructure as Code
5. **Terraform**: Multi-cloud IaC

### Resource Management Commands
```bash
# Create multi-service account
az cognitiveservices account create \
  --name myai-account \
  --resource-group rg-ai \
  --kind CognitiveServices \
  --sku S0 \
  --location eastus

# Create specific service
az cognitiveservices account create \
  --name my-vision \
  --resource-group rg-ai \
  --kind ComputerVision \
  --sku F0 \
  --location eastus

# List keys
az cognitiveservices account keys list \
  --name myai-account \
  --resource-group rg-ai

# Regenerate keys
az cognitiveservices account keys regenerate \
  --name myai-account \
  --resource-group rg-ai \
  --key-name key1

# Show usage
az cognitiveservices account list-usage \
  --name myai-account \
  --resource-group rg-ai
```

### Monitoring and Diagnostics
```python
# Application Insights Integration
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=<key>'
))

# Custom Metrics
from applicationinsights import TelemetryClient
tc = TelemetryClient('<instrumentation_key>')
tc.track_metric('api_latency', 150)
tc.track_metric('accuracy', 0.95)

# Diagnostic Settings (Azure Monitor)
{
  "logs": [
    {
      "category": "Audit",
      "enabled": true,
      "retentionPolicy": {
        "enabled": true,
        "days": 30
      }
    }
  ],
  "metrics": [
    {
      "category": "AllMetrics",
      "enabled": true
    }
  ]
}
```

## Monitor and optimize Azure AI services

### Key Metrics to Track
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Total Calls | API requests | Sudden spike/drop |
| Successful Calls | Non-error responses | < 99% |
| Total Errors | 4xx and 5xx errors | > 1% |
| Latency | Response time | > 1000ms |
| Throttled Calls | Rate limit hits | > 0 |

### Cost Optimization Strategies
1. **Choose appropriate tier**
   - F0 (Free): Development and testing
   - S0: Production with pay-as-you-go
   - Commitment tiers: Predictable workloads

2. **Implement caching**
```python
import hashlib
import json
from azure.core.exceptions import HttpResponseError
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_analysis(text_hash):
    return client.analyze_sentiment([text])

def analyze_with_cache(text):
    text_hash = hashlib.md5(text.encode()).hexdigest()
    return cached_analysis(text_hash)
```

3. **Batch processing**
```python
# Process multiple items in single call
documents = [
    {"id": "1", "text": "Text 1"},
    {"id": "2", "text": "Text 2"},
    # Up to 25 documents
]
results = client.analyze_sentiment(documents)
```

### Sample Exam Questions - Domain 1

**Q1**: You need to ensure that your Cognitive Services resources can only be accessed from your virtual network. What should you configure?
- A) API Management
- B) Private Endpoints ✓
- C) Azure Front Door
- D) Application Gateway

**Q2**: Which authentication method should you use for production workloads?
- A) Subscription keys
- B) Managed Identity ✓
- C) SAS tokens
- D) Basic authentication

**Q3**: You need to track custom business metrics for your AI service. What should you use?
- A) Azure Monitor Logs
- B) Application Insights Custom Metrics ✓
- C) Event Hub
- D) Storage Analytics

---

# Domain 2: Implement Computer Vision Solutions (20-25%)

## Analyze images using Computer Vision

### Image Analysis Features
```python
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures

# All available features
features = [
    VisualFeatures.CAPTION,         # Generate image description
    VisualFeatures.DENSE_CAPTIONS,  # Multiple regional captions
    VisualFeatures.TAGS,            # Content tags
    VisualFeatures.OBJECTS,         # Object detection
    VisualFeatures.PEOPLE,          # People detection
    VisualFeatures.SMART_CROPS,     # Intelligent cropping
    VisualFeatures.READ             # OCR text extraction
]

# Analyze image
result = client.analyze(
    image_data=image_data,
    visual_features=features,
    language="en",
    gender_neutral_caption=True,
    smart_crops_aspect_ratios=[0.9, 1.33]  # Portrait and landscape
)
```

### OCR Capabilities Comparison
| Feature | Read API | OCR API (deprecated) |
|---------|----------|---------------------|
| Handwritten | Yes | No |
| Languages | 100+ | 25 |
| Async | Yes | No |
| Large docs | Yes | No |
| Tables | Yes | Limited |

### Spatial Analysis (Computer Vision for edge)
```python
# Spatial operations
operations = [
    "PersonCount",           # Count people in zone
    "PersonCrossingLine",    # Detect line crossing
    "PersonCrossingPolygon", # Detect zone entry/exit
    "PersonDistance"         # Social distancing
]

# Configuration example
spatial_config = {
    "operations": [
        {
            "operationId": "1",
            "kind": "PersonCrossingLine",
            "line": {
                "start": {"x": 0.3, "y": 0.5},
                "end": {"x": 0.7, "y": 0.5}
            }
        }
    ]
}
```

## Extract text from images using OCR

### Read API Best Practices
```python
# Async processing for large documents
poller = client.begin_read(
    image_url,
    language="en",
    pages=["1-3", "5"],  # Specific pages
    reading_order="natural",  # or "basic"
    model_version="2022-04-30"  # Latest model
)

result = poller.result()

# Process results
for page in result.analyze_result.read_results:
    print(f"Page {page.page} - {page.width}x{page.height}")
    
    for line in page.lines:
        print(f"Line: {line.text}")
        print(f"Bounding box: {line.bounding_box}")
        
        for word in line.words:
            print(f"  Word: {word.text} (confidence: {word.confidence})")
```

## Train custom image models using Custom Vision

### Project Types
1. **Classification**
   - Multiclass: One tag per image
   - Multilabel: Multiple tags per image

2. **Object Detection**
   - Identify and locate objects
   - Returns bounding boxes

### Training Requirements
| Project Type | Minimum Images | Recommended |
|-------------|----------------|-------------|
| Classification | 5 per tag | 50+ per tag |
| Object Detection | 15 per tag | 50+ per tag |

### Training Code
```python
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

# Create project
project = trainer.create_project(
    "Product Classifier",
    domain_id=general_domain_id,
    classification_type="Multiclass",
    target_export_platforms=["CoreML", "TensorFlow", "ONNX"]
)

# Upload and tag images
for image_path, tag_name in training_data:
    with open(image_path, "rb") as image:
        trainer.create_images_from_data(
            project.id,
            image.read(),
            tag_ids=[tag_map[tag_name]]
        )

# Train
iteration = trainer.train_project(project.id)
while iteration.status != "Completed":
    iteration = trainer.get_iteration(project.id, iteration.id)
    time.sleep(1)

# Publish
trainer.publish_iteration(
    project.id,
    iteration.id,
    "production",
    prediction_resource_id
)
```

## Detect faces using Face service

### ⚠️ Important: Restricted Access
Face API now requires approval for:
- Face recognition
- Face identification
- Face verification

### Available Features (Unrestricted)
```python
# Face detection with attributes
faces = face_client.face.detect_with_stream(
    image,
    return_face_id=True,
    return_face_landmarks=True,
    return_face_attributes=[
        'age',
        'gender',
        'smile',
        'facialHair',
        'glasses',
        'emotion',
        'hair',
        'makeup',
        'accessories',
        'blur',
        'exposure',
        'noise',
        'headPose'
    ],
    detection_model='detection_03',
    recognition_model='recognition_04'
)

for face in faces:
    print(f"Face ID: {face.face_id}")
    print(f"Age: {face.face_attributes.age}")
    print(f"Emotion: {max(face.face_attributes.emotion.as_dict().items(), key=lambda x: x[1])}")
```

### Sample Exam Questions - Domain 2

**Q1**: Which visual feature should you use to generate a natural language description of an image?
- A) Tags
- B) Objects
- C) Caption ✓
- D) Categories

**Q2**: What is the minimum number of images required to train a Custom Vision object detection model?
- A) 5 images total
- B) 15 images per tag ✓
- C) 50 images per tag
- D) 100 images total

**Q3**: Which API should you use to extract handwritten text from a PDF?
- A) OCR API
- B) Read API ✓
- C) Recognize Text API
- D) Form Recognizer

---

# Domain 3: Implement Natural Language Processing Solutions (20-25%)

## Analyze text using Language service

### Text Analytics Features
```python
from azure.ai.textanalytics import TextAnalyticsClient

# Sentiment Analysis with Opinion Mining
result = client.analyze_sentiment(
    documents,
    show_opinion_mining=True,
    language="en"
)

for doc in result:
    print(f"Document sentiment: {doc.sentiment}")
    print(f"Scores: Positive={doc.confidence_scores.positive:.2f}")
    
    for sentence in doc.sentences:
        print(f"  Sentence: {sentence.sentiment}")
        for opinion in sentence.mined_opinions:
            print(f"    Target: {opinion.target.text} - {opinion.target.sentiment}")
            for assessment in opinion.assessments:
                print(f"      Assessment: {assessment.text} - {assessment.sentiment}")

# Key Phrase Extraction
key_phrases = client.extract_key_phrases(documents)

# Named Entity Recognition
entities = client.recognize_entities(documents)
for entity in entities[0].entities:
    print(f"Entity: {entity.text}")
    print(f"Category: {entity.category}")
    print(f"Subcategory: {entity.subcategory}")
    print(f"Confidence: {entity.confidence_score}")

# Entity Linking
linked_entities = client.recognize_linked_entities(documents)
for entity in linked_entities[0].entities:
    print(f"Name: {entity.name}")
    print(f"Wikipedia URL: {entity.url}")
    print(f"Data source: {entity.data_source}")

# PII Detection
pii_entities = client.recognize_pii_entities(documents)
for entity in pii_entities[0].entities:
    print(f"PII: {entity.text}")
    print(f"Category: {entity.category}")
    
# Healthcare entities (Text Analytics for Health)
poller = client.begin_analyze_healthcare_entities(documents)
result = poller.result()
```

### Custom NER and Classification
```python
from azure.ai.language.textanalytics import TextAnalyticsClient

# Custom NER
poller = client.begin_recognize_custom_entities(
    documents,
    project_name="custom-ner-project",
    deployment_name="production"
)

# Custom Classification
poller = client.begin_single_label_classify(
    documents,
    project_name="document-classifier",
    deployment_name="production"
)
```

## Process speech using Speech service

### Speech-to-Text Patterns
```python
import azure.cognitiveservices.speech as speechsdk

# Real-time recognition
speech_config = speechsdk.SpeechConfig(
    subscription=key,
    region=region
)
speech_config.speech_recognition_language = "en-US"

# Continuous recognition
def continuous_recognition():
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
    
    def recognized(evt):
        print(f"Recognized: {evt.result.text}")
    
    def recognizing(evt):
        print(f"Recognizing: {evt.result.text}")
    
    recognizer.recognized.connect(recognized)
    recognizer.recognizing.connect(recognizing)
    
    recognizer.start_continuous_recognition()

# Batch transcription
from azure.ai.speechservices import BatchClient

batch_client = BatchClient(endpoint, credential)
transcription = batch_client.transcriptions.create(
    display_name="Batch Transcription",
    locale="en-US",
    content_urls=["https://storage.blob.core.windows.net/audio/file.wav"],
    properties={
        "diarizationEnabled": True,
        "wordLevelTimestampsEnabled": True,
        "punctuationMode": "DictatedAndAutomatic"
    }
)
```

### Text-to-Speech
```python
# Neural voices
speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=audio_config
)

# SSML for advanced control
ssml = """
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
    <voice name='en-US-JennyNeural'>
        <prosody rate='-10%' pitch='+5%'>
            Hello, this is a customized voice output.
        </prosody>
        <break time='500ms'/>
        <emphasis level='strong'>Important message!</emphasis>
    </voice>
</speak>
"""

result = synthesizer.speak_ssml_async(ssml).get()
```

## Translate text and speech

### Text Translation
```python
from azure.ai.translation.text import TextTranslationClient

# Translate to multiple languages
response = client.translate(
    body=["Hello world"],
    to_language=["es", "fr", "de", "ja"],
    from_language="en",
    profanity_action="Marked",
    profanity_marker="Tag",
    include_alignment=True,
    include_sentence_length=True
)

# Document translation
from azure.ai.translation.document import DocumentTranslationClient

poller = client.begin_translation(
    source_url="https://storage.blob.core.windows.net/source",
    target_url="https://storage.blob.core.windows.net/target",
    target_language="es",
    source_language="en"
)
```

### Speech Translation
```python
# Real-time speech translation
translation_config = speechsdk.translation.SpeechTranslationConfig(
    subscription=key,
    region=region
)
translation_config.speech_recognition_language = "en-US"
translation_config.add_target_language("es")
translation_config.add_target_language("fr")

recognizer = speechsdk.translation.TranslationRecognizer(
    translation_config=translation_config
)

def recognized(evt):
    print(f"Original: {evt.result.text}")
    print(f"Spanish: {evt.result.translations['es']}")
    print(f"French: {evt.result.translations['fr']}")

recognizer.recognized.connect(recognized)
```

## Implement Conversational Language Understanding (CLU)

### CLU vs LUIS
- CLU is the successor to LUIS
- Better multilingual support
- Improved entity extraction
- Orchestration workflows

### Implementation
```python
from azure.ai.language.conversations import ConversationAnalysisClient

# Analyze conversation
result = client.analyze_conversation(
    task={
        "kind": "Conversation",
        "analysisInput": {
            "conversationItem": {
                "id": "1",
                "participantId": "user",
                "text": "Book a flight to Seattle tomorrow"
            }
        },
        "parameters": {
            "projectName": "travel-booking",
            "deploymentName": "production",
            "verbose": True
        }
    }
)

# Extract results
top_intent = result["result"]["prediction"]["topIntent"]
entities = result["result"]["prediction"]["entities"]

for entity in entities:
    print(f"Entity: {entity['text']}")
    print(f"Category: {entity['category']}")
    print(f"Confidence: {entity['confidenceScore']}")
```

### Sample Exam Questions - Domain 3

**Q1**: Which feature should you use to identify and categorize personal information in text?
- A) Named Entity Recognition
- B) PII Detection ✓
- C) Key Phrase Extraction
- D) Sentiment Analysis

**Q2**: What is required for real-time speech translation?
- A) Speech SDK with TranslationRecognizer ✓
- B) Translator Text API only
- C) Batch transcription API
- D) Custom Speech model

**Q3**: Which service replaced LUIS for conversational AI?
- A) QnA Maker
- B) Bot Framework
- C) Conversational Language Understanding (CLU) ✓
- D) Custom Neural Voice

---

# Domain 4: Implement Knowledge Mining and Document Intelligence (15-20%)

## Implement Azure Cognitive Search

### Index Creation
```python
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration
)

# Define index schema
index = SearchIndex(
    name="products-index",
    fields=[
        SimpleField(name="id", type="Edm.String", key=True),
        SearchableField(name="title", type="Edm.String", 
                       analyzer_name="en.microsoft"),
        SearchableField(name="description", type="Edm.String"),
        SimpleField(name="price", type="Edm.Double", 
                   filterable=True, sortable=True),
        SimpleField(name="category", type="Edm.String", 
                   filterable=True, facetable=True),
        SearchField(name="description_vector", 
                   type="Collection(Edm.Single)",
                   searchable=True,
                   vector_search_dimensions=1536,
                   vector_search_profile_name="vector-profile")
    ],
    vector_search=VectorSearch(
        profiles=[VectorSearchProfile(
            name="vector-profile",
            algorithm_configuration_name="hnsw"
        )],
        algorithms=[HnswAlgorithmConfiguration(
            name="hnsw",
            parameters={"m": 4, "efConstruction": 400, "metric": "cosine"}
        )]
    )
)
```

### AI Enrichment Pipeline
```python
# Skillset definition
skillset = {
    "name": "document-skillset",
    "skills": [
        {
            "@odata.type": "#Microsoft.Skills.Text.V3.EntityRecognitionSkill",
            "name": "entities",
            "context": "/document",
            "inputs": [{"name": "text", "source": "/document/content"}],
            "outputs": [
                {"name": "persons", "targetName": "people"},
                {"name": "organizations", "targetName": "organizations"},
                {"name": "locations", "targetName": "locations"}
            ]
        },
        {
            "@odata.type": "#Microsoft.Skills.Text.KeyPhraseExtractionSkill",
            "name": "keyphrases",
            "context": "/document",
            "inputs": [{"name": "text", "source": "/document/content"}],
            "outputs": [{"name": "keyPhrases", "targetName": "keyPhrases"}]
        },
        {
            "@odata.type": "#Microsoft.Skills.Text.V3.SentimentSkill",
            "name": "sentiment",
            "context": "/document",
            "inputs": [{"name": "text", "source": "/document/content"}],
            "outputs": [{"name": "sentiment", "targetName": "sentiment"}]
        },
        {
            "@odata.type": "#Microsoft.Skills.Vision.OcrSkill",
            "name": "ocr",
            "context": "/document/normalized_images/*",
            "inputs": [{"name": "image", "source": "/document/normalized_images/*"}],
            "outputs": [{"name": "text", "targetName": "text"}]
        }
    ],
    "cognitiveServices": {
        "@odata.type": "#Microsoft.Azure.Search.CognitiveServicesByKey",
        "key": cognitive_services_key
    }
}
```

### Search Queries
```python
from azure.search.documents import SearchClient

# Semantic search
results = search_client.search(
    search_text="comfortable running shoes",
    query_type="semantic",
    semantic_configuration_name="my-semantic-config",
    select=["title", "description", "price"],
    filter="category eq 'Footwear' and price lt 150",
    order_by=["price desc"],
    top=10
)

# Vector search
from azure.search.documents.models import VectorizedQuery

vector_query = VectorizedQuery(
    vector=embedding_vector,
    k_nearest_neighbors=5,
    fields="description_vector"
)

results = search_client.search(
    search_text="athletic shoes",
    vector_queries=[vector_query],
    select=["title", "description", "price"],
    top=10
)

# Faceted search
results = search_client.search(
    search_text="*",
    facets=["category", "price_range"],
    top=0  # Just get facets, no documents
)

for facet in results.get_facets()["category"]:
    print(f"{facet['value']}: {facet['count']}")
```

## Extract data using Form Recognizer

### Pre-built Models
```python
from azure.ai.formrecognizer import DocumentAnalysisClient

# Invoice processing
poller = client.begin_analyze_document(
    "prebuilt-invoice",
    document=document
)
result = poller.result()

for invoice in result.documents:
    print(f"Vendor: {invoice.fields.get('VendorName').value}")
    print(f"Total: {invoice.fields.get('InvoiceTotal').value}")
    
    # Line items
    for item in invoice.fields.get("Items").value:
        print(f"  - {item.value.get('Description').value}: "
              f"{item.value.get('Amount').value}")

# Layout analysis
poller = client.begin_analyze_document(
    "prebuilt-layout",
    document=document
)
result = poller.result()

for table in result.tables:
    print(f"Table with {table.row_count} rows and {table.column_count} columns")
    for cell in table.cells:
        print(f"  Cell[{cell.row_index},{cell.column_index}]: {cell.content}")
```

### Custom Models
```python
from azure.ai.formrecognizer import DocumentModelAdministrationClient

# Train custom model
poller = admin_client.begin_build_document_model(
    model_id="custom-invoice-model",
    blob_container_url=container_sas_url,
    build_mode="template"  # or "neural" for better accuracy
)
model = poller.result()

# Compose models
poller = admin_client.begin_compose_document_model(
    model_id="composed-model",
    component_model_ids=["model1", "model2", "model3"]
)
```

### Sample Exam Questions - Domain 4

**Q1**: Which enrichment skill extracts organizations and people from text?
- A) KeyPhraseExtractionSkill
- B) EntityRecognitionSkill ✓
- C) SentimentSkill
- D) LanguageDetectionSkill

**Q2**: What is the purpose of a knowledge store in Cognitive Search?
- A) Cache search results
- B) Store enriched data in tables and blobs ✓
- C) Store user queries
- D) Store index definitions

**Q3**: Which build mode provides better accuracy for custom Form Recognizer models?
- A) Template
- B) Neural ✓
- C) Layout
- D) Structured

---

# Domain 5: Implement Generative AI Solutions (15-20%)

## Use Azure OpenAI Service

### Model Selection
| Model | Best For | Context Window | Training Data |
|-------|----------|---------------|---------------|
| GPT-4o | Complex reasoning, multimodal | 128K | Oct 2023 |
| GPT-4 | Complex tasks | 128K | Sep 2021 |
| GPT-3.5-Turbo | Fast responses | 16K | Sep 2021 |
| DALL-E 3 | Image generation | - | - |
| Whisper | Transcription | - | - |
| Text-Embedding-3 | Embeddings | 8K | - |

### Implementation Patterns
```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=api_key,
    api_version="2024-02-01",
    azure_endpoint=endpoint
)

# Chat completion
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing"}
    ],
    temperature=0.7,
    max_tokens=500,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
)

# Function calling
functions = [
    {
        "name": "get_weather",
        "description": "Get current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["location"]
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    functions=functions,
    function_call="auto"
)

# Image generation
response = client.images.generate(
    model="dall-e-3",
    prompt="A serene landscape with mountains and a lake at sunset",
    size="1024x1024",
    quality="hd",
    style="natural",
    n=1
)

# Embeddings
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Text to embed",
    encoding_format="float"
)
```

## Implement Retrieval Augmented Generation (RAG)

### RAG Architecture
```
1. Document Ingestion → Chunking → Embeddings → Vector Store
2. Query → Query Embedding → Similarity Search → Context Retrieval
3. Context + Query → LLM → Generated Response
```

### Implementation
```python
class RAGSystem:
    def __init__(self, search_client, openai_client):
        self.search = search_client
        self.openai = openai_client
    
    def generate_embedding(self, text):
        response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def retrieve_context(self, query, top_k=5):
        query_embedding = self.generate_embedding(query)
        
        results = self.search.search(
            vector_queries=[VectorizedQuery(
                vector=query_embedding,
                k_nearest_neighbors=top_k,
                fields="content_vector"
            )],
            select=["content", "source", "page"]
        )
        
        return [{"content": r["content"], "source": r["source"]} 
                for r in results]
    
    def generate_response(self, query, context):
        context_text = "\n\n".join([doc["content"] for doc in context])
        
        messages = [
            {"role": "system", "content": 
             "Answer questions based on the provided context. "
             "If the answer isn't in the context, say so."},
            {"role": "user", "content": 
             f"Context:\n{context_text}\n\nQuestion: {query}"}
        ]
        
        response = self.openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.3
        )
        
        return response.choices[0].message.content
```

## Implement prompt engineering

### Techniques
```python
# 1. Zero-shot
prompt = "Classify the sentiment: 'This product exceeded my expectations!'"

# 2. Few-shot
prompt = """
Classify the sentiment:
'Great service!' -> Positive
'Terrible experience' -> Negative
'It was okay' -> Neutral
'This product exceeded my expectations!' ->
"""

# 3. Chain of Thought (CoT)
prompt = """
Solve step by step:
If a train travels 60 miles in 1.5 hours, what is its average speed?

Step 1: Identify what we need to find (average speed)
Step 2: Recall the formula (speed = distance/time)
Step 3: Apply the formula (60 miles / 1.5 hours)
Step 4: Calculate (40 mph)
"""

# 4. System prompts for consistency
system_prompt = """
You are a technical documentation writer. Follow these rules:
1. Use clear, concise language
2. Include code examples
3. Avoid jargon
4. Structure with headers and bullet points
"""

# 5. Output formatting
prompt = """
Extract information from this text and format as JSON:
"John Doe, age 30, works as a software engineer in Seattle."

Output format:
{
  "name": "",
  "age": 0,
  "occupation": "",
  "location": ""
}
"""
```

## Responsible AI for Generative Solutions

### Content Filtering
```python
# Azure OpenAI content filtering
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    # Content filtering happens automatically
)

# Check content filter results
if response.choices[0].finish_reason == "content_filter":
    print("Response filtered due to content policy")

# Custom content filtering
from azure.ai.contentsafety import ContentSafetyClient

safety_client = ContentSafetyClient(endpoint, credential)
result = safety_client.analyze_text(
    text=user_input,
    categories=["Hate", "SelfHarm", "Sexual", "Violence"],
    output_type="FourSeverityLevels"
)

if any(score >= 4 for score in result.categories_analysis):
    raise ValueError("Content violates safety policies")
```

### Sample Exam Questions - Domain 5

**Q1**: What is the maximum context window for GPT-4?
- A) 4K tokens
- B) 8K tokens
- C) 32K tokens
- D) 128K tokens ✓

**Q2**: Which technique improves reasoning in LLMs?
- A) Increasing temperature
- B) Chain of Thought prompting ✓
- C) Reducing max_tokens
- D) Disabling stop sequences

**Q3**: What is the primary purpose of embeddings in RAG?
- A) Generate responses
- B) Semantic similarity search ✓
- C) Content filtering
- D) Token counting

---

# 📝 Practice Exam Questions

## Set 1: Mixed Domains

**Q1**: You need to process 10,000 documents per day. Which tier should you choose?
- A) F0 (Free)
- B) S0 (Standard) ✓
- C) S1 (Premium)
- D) Commitment tier

**Q2**: Which service provides real-time translation of spoken language?
- A) Translator Text
- B) Speech Service with TranslationRecognizer ✓
- C) Language Understanding
- D) Conversational Language Understanding

**Q3**: You need to extract tables from scanned PDFs. What should you use?
- A) Computer Vision OCR
- B) Form Recognizer Layout API ✓
- C) Cognitive Search
- D) Custom Vision

**Q4**: How do you implement semantic search in Cognitive Search?
- A) Use fuzzy matching
- B) Enable semantic configuration ✓
- C) Use regular expressions
- D) Implement custom scoring

**Q5**: Which is NOT a valid content filter category in Azure OpenAI?
- A) Hate
- B) Violence
- C) Profanity ✓
- D) Self-harm

## Set 2: Scenario-Based

**Scenario 1**: Your company needs to build a customer service chatbot that:
- Understands natural language in 5 languages
- Answers from a knowledge base
- Escalates complex issues to humans

**Solution Components**:
- CLU for intent recognition
- Translator for multi-language support
- Cognitive Search for knowledge base
- Azure OpenAI for response generation
- Bot Framework for orchestration

**Scenario 2**: You're building a document processing pipeline that:
- Extracts data from invoices
- Validates against business rules
- Stores in a database
- Generates reports

**Solution Components**:
- Form Recognizer with prebuilt-invoice model
- Azure Functions for validation logic
- Cosmos DB for storage
- Power BI for reporting

---

# 🎯 Exam Day Tips

## Before the Exam
1. **Review all domains** - Focus on your weak areas
2. **Take practice tests** - MeasureUp, Pluralsight
3. **Hands-on practice** - Actually build solutions
4. **Review limits** - Know the tier limitations
5. **Sleep well** - Don't cram the night before

## During the Exam
1. **Read carefully** - Look for keywords like "minimize cost" or "maximize accuracy"
2. **Eliminate wrong answers** - Often 2 are obviously wrong
3. **Flag difficult questions** - Return to them later
4. **Watch for negatives** - "Which is NOT..." questions
5. **Consider all requirements** - Security, cost, performance

## Time Management
- 100 minutes for ~50 questions = 2 minutes per question
- Spend 1 minute reading and answering
- Flag complex questions for review
- Leave 10-15 minutes for review

## Common Traps
1. **Service confusion** - Computer Vision vs Custom Vision
2. **Deprecated features** - LUIS vs CLU, OCR API vs Read API
3. **Tier limitations** - Free tier restrictions
4. **Regional availability** - Not all services in all regions
5. **Preview features** - Generally not in exam

---

# 📚 Study Resources

## Official Microsoft
1. [AI-102 Exam Page](https://learn.microsoft.com/certifications/exams/ai-102)
2. [Microsoft Learn Path](https://learn.microsoft.com/training/paths/azure-ai-engineer/)
3. [Azure AI Documentation](https://learn.microsoft.com/azure/ai-services/)
4. [GitHub Samples](https://github.com/Azure-Samples)

## Practice Tests
1. **MeasureUp** - Official practice test provider
2. **Pluralsight** - Skill assessments
3. **Udemy** - Practice exams
4. **WhizLabs** - Question banks

## Community Resources
1. **Reddit** - r/AzureCertification
2. **Discord** - Azure community servers
3. **YouTube** - John Savill, Tim Warner
4. **Blogs** - Thomas Maurer, Sam Cogan

## Hands-On Labs
1. **Microsoft Learn Sandbox** - Free environment
2. **Azure Free Account** - $200 credit
3. **GitHub Codespaces** - Cloud development
4. **Local Development** - VS Code + Extensions

---

# ✅ Final Checklist

## Must Know Concepts
- [ ] All Azure AI services and their use cases
- [ ] Authentication methods and security
- [ ] Pricing tiers and limitations
- [ ] REST API vs SDK patterns
- [ ] Batch vs real-time processing
- [ ] Custom vs pre-built models
- [ ] Monitoring and optimization
- [ ] Responsible AI principles

## Hands-On Experience
- [ ] Built at least one solution per service
- [ ] Implemented security best practices
- [ ] Deployed to production-like environment
- [ ] Monitored and optimized performance
- [ ] Handled errors and edge cases

## Exam Readiness
- [ ] Completed all Microsoft Learn modules
- [ ] Scored >80% on practice tests
- [ ] Reviewed all wrong answers
- [ ] Can explain concepts to others
- [ ] Comfortable with all domains

---

**Good luck with your AI-102 exam! 🚀**

*Remember: The exam tests practical knowledge. Build real solutions to truly understand the concepts.*