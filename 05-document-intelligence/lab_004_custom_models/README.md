# Lab 004: Custom Document Intelligence Models

**Date Completed**: 2025-07-23  
**Duration**: 45 minutes  
**Model**: Custom extraction model with template-based training

## 🎯 Objectives
- Train a custom Document Intelligence model for specific form types
- Extract custom fields from purchase order documents
- Achieve high-accuracy field extraction for business automation

## 🛠️ Setup Details

### Storage Configuration
- **Storage Account**: ai102form23681
- **Container**: sampleforms
- **Training Data**: 5 labeled purchase order forms

### Model Configuration
- **Model ID**: testingmodel
- **Build Mode**: Template
- **Document Intelligence Resource**: doc-intelligence-20250723
- **Resource Group**: cog-search-language-exe

## 📊 Results

### Extracted Fields (with Confidence Scores)
- **Merchant**: Hero Limited (99%)
- **CompanyName**: Yoga for You (99.1%)
- **CompanyPhoneNumber**: 234-986-6454 (99.5%)
- **Total**: $7350.00 (99.4%)
- **Tax**: $600.00 (99.3%)
- **Subtotal**: $6750.00 (99.4%)
- **PurchaseOrderNumber**: 3929423 (99.4%)
- **VendorName**: Seth Stanley (99%)
- **DatedAs**: 04/04/2020 (99.4%)
- **Quantity**: 50.0 (99%)
- **Website**: www.herolimited.com (99%)
- **Email**: accounts@herolimited.com (94.9%)
- **PhoneNumber**: 555-348-6512 (99%)
- **Signature**: Josh Granger (45.2%)
- **CompanyAddress**: 343 E Winter Road Seattle, WA 93849 (48.6%)

### Model Performance
- **Overall Document Confidence**: 81.8%
- **High-Confidence Fields**: 13/15 (>90% confidence)
- **Low-Confidence Fields**: Signature and Address (expected for handwritten/complex text)

## 🔑 Key Learnings

1. **Template-Based Training**
   - Requires consistent form layout
   - Excellent for structured documents
   - Fast training with only 5 samples

2. **Field Extraction Accuracy**
   - Numeric and structured data: 99%+ accuracy
   - Email addresses: 94%+ accuracy
   - Handwritten signatures: ~45% (consider alternative approaches)
   - Multi-line addresses: ~48% (may need region-based extraction)

3. **Business Applications**
   - Purchase order automation
   - Invoice processing
   - Form digitization
   - Data entry elimination

## 💻 Code Implementation

```python
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Initialize client
client = DocumentAnalysisClient(
    endpoint=endpoint, 
    credential=AzureKeyCredential(key)
)

# Analyze document
response = client.begin_analyze_document_from_url(
    model_id="testingmodel", 
    document_url=form_url
)
result = response.result()

# Extract fields
for document in result.documents:
    for name, field in document.fields.items():
        print(f"{name}: {field.value} ({field.confidence*100:.1f}%)")
```

## 🎓 Skills Developed
- Custom model training in Document Intelligence Studio
- Azure Blob Storage setup for training data
- Label file creation and management
- Model performance evaluation
- Integration with Python SDK

## 📈 Business Impact
- **Time Saved**: ~5 minutes per document
- **Accuracy**: 99%+ for critical financial fields
- **Scalability**: Process thousands of documents per hour
- **ROI**: Eliminate manual data entry costs

## 🔗 Resources
- [Training Data (SAS URI)](https://ai102form23681.blob.core.windows.net/sampleforms?se=2026-01-01T00%3A00%3A00Z&sp=rwl&sv=2022-11-02&sr=c&sig=wtUHS8TOKTzjYL%2BlSxH7qhBUOohwpBALgO6g%2Bli20TY%3D)
- [Test Form](https://github.com/MicrosoftLearning/mslearn-ai-information-extraction/blob/main/Labfiles/custom-doc-intelligence/test1.jpg?raw=true)
- Model ID: testingmodel

---
*Part of Azure AI Engineer Associate (AI-102) certification journey*