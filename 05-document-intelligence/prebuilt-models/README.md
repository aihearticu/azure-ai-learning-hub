# Lab 003: Prebuilt Document Intelligence Model

## Metadata
- **Date Completed**: 2025-07-23
- **Category**: Document Processing
- **Difficulty**: Beginner
- **Time Taken**: 30 minutes
- **Prerequisites**: 
  - Azure subscription
  - Python 3.x
  - Azure Document Intelligence resource

## Azure Services Used
- **Primary**: Azure Document Intelligence (Form Recognizer)
- **Supporting**: Azure AI services
- **Cost Estimate**: Free tier (F0) - 500 pages/month free

## Business Scenario
### Problem Statement
Organizations need to extract structured data from invoices, receipts, and other documents automatically without manual data entry.

### Use Cases
- Invoice processing automation
- Receipt data extraction
- Accounts payable automation
- Document digitization workflows

## Implementation Summary

### What It Does
Uses prebuilt AI models to extract key information from standard document types (invoices, receipts, business cards, ID documents) without training custom models.

### Results Achieved
Successfully extracted from sample invoice:
- **Vendor Name**: CONTOSO LTD. (93.7% confidence)
- **Customer Name**: MICROSOFT CORPORATION (91.9% confidence)  
- **Invoice Total**: $110.0 (96.9% confidence)

## Code Implementation

### Key Code Pattern
```python
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Create client
client = DocumentAnalysisClient(
    endpoint=endpoint, 
    credential=AzureKeyCredential(key)
)

# Analyze document
poller = client.begin_analyze_document_from_url(
    "prebuilt-invoice",  # Model ID
    document_url,
    locale="en-US"
)

# Get results
result = poller.result()
for document in result.documents:
    vendor = document.fields.get("VendorName")
    if vendor:
        print(f"Vendor: {vendor.value}, confidence: {vendor.confidence}")
```

## Key Learnings

### What Worked Well
1. Prebuilt models work immediately - no training required
2. High confidence scores (90%+) for standard fields
3. Supports URLs and local files
4. Multiple document types available

### Available Prebuilt Models
- `prebuilt-invoice` - Invoices
- `prebuilt-receipt` - Receipts  
- `prebuilt-businessCard` - Business cards
- `prebuilt-idDocument` - IDs/Passports
- `prebuilt-document` - General documents
- `prebuilt-layout` - Document structure
- `prebuilt-read` - Text extraction

### Best Practices
- ✅ Use prebuilt models for standard document types
- ✅ Check confidence scores before using data
- ✅ Handle missing fields gracefully
- ❌ Don't use for non-standard formats (train custom model instead)

## Performance Metrics
- Processing time: ~2-3 seconds per document
- Accuracy: 90%+ for standard fields
- Supported formats: PDF, JPEG, PNG, TIFF, BMP

## Integration Opportunities
### Combines Well With
- **Logic Apps**: Automated document workflows
- **Cognitive Search**: Make documents searchable
- **Cosmos DB**: Store extracted data
- **Power Automate**: No-code automation

## Next Steps
- Try other prebuilt models (receipts, IDs)
- Process batch documents
- Build custom model for unique formats (Lab 04)

## Resources
- [Document Intelligence Documentation](https://docs.microsoft.com/azure/applied-ai-services/form-recognizer/)
- [Prebuilt Models Reference](https://docs.microsoft.com/azure/applied-ai-services/form-recognizer/concept-model-overview)
- [Python SDK Reference](https://docs.microsoft.com/python/api/azure-ai-formrecognizer/)

## Twitter Summary
"Azure Document Intelligence extracted invoice data with 90%+ accuracy in seconds - no training needed! Just point at PDF and get structured JSON. Magic for accounts payable automation 📄✨"

---
*Part of Azure AI Engineer Learning Journey*