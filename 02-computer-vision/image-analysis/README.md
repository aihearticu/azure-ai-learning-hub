# Lab 001: Image Analysis with Computer Vision

## Metadata
- **Date Started**: In Progress
- **Category**: Computer Vision
- **Difficulty**: Beginner
- **Time Estimate**: 1-2 hours
- **Prerequisites**: 
  - Azure subscription
  - Python 3.x
  - Azure AI Services or Computer Vision resource

## Azure Services Used
- **Primary**: Azure Computer Vision
- **Supporting**: Azure AI Services
- **Cost Estimate**: Free tier (F0) - 5,000 transactions/month

## Business Scenario
### Problem Statement
Organizations need to automatically analyze and understand the content of images for various applications like content moderation, accessibility, and automated tagging.

### Use Cases
- Automatic image captioning for accessibility
- Content moderation for user uploads
- Object detection for inventory management
- People counting for occupancy monitoring

## Lab Objectives
1. Set up Azure Computer Vision service
2. Analyze images to generate captions
3. Extract tags and object information
4. Detect people in images
5. Annotate images with bounding boxes

## Implementation Structure

### Files Included
```
image-analysis/
├── src/
│   └── image-analysis.py    # Main implementation file
├── images/                  # Sample images for testing
│   ├── street.jpg
│   ├── building.jpg
│   └── person.jpg
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Key Features to Implement
- Image caption generation
- Tag extraction with confidence scores
- Object detection with bounding boxes
- People detection and counting
- Visual annotation of results

## Setup Instructions

1. **Create Azure Resource**
   ```bash
   az cognitiveservices account create \
     --name my-vision-service \
     --resource-group rg-ai-learning \
     --kind ComputerVision \
     --sku F0 \
     --location eastus
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   # Create .env file with:
   AI_SERVICE_ENDPOINT=your-endpoint
   AI_SERVICE_KEY=your-key
   ```

## Expected Results
- Automatic image descriptions
- List of relevant tags
- Detected objects with locations
- Annotated images with bounding boxes

## Next Steps
- Complete the implementation
- Test with various image types
- Explore advanced features like OCR
- Move to custom vision models

---
*Part of Azure AI Engineer Learning Journey*