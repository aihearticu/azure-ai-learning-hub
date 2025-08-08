# Lab 01: Analyze Images with Azure AI Vision

## Overview
This lab demonstrates how to use Azure AI Vision service to analyze images and extract various insights including captions, tags, objects, and people detection.

## Prerequisites
- Azure subscription (Free tier F0 supported)
- Python 3.8+
- Azure AI Vision resource

## Azure Setup Instructions

### 1. Create Azure AI Vision Resource

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "+ Create a resource"
3. Search for "Computer Vision" 
4. Click "Create"
5. Configure:
   - **Subscription**: Your Azure subscription
   - **Resource group**: Create new or use existing
   - **Region**: East US, West US, or other supported region
   - **Name**: Choose a unique name (e.g., `vision-lab-{your-initials}`)
   - **Pricing tier**: F0 (Free) - 20 calls per minute, 5K calls per month

6. Review and create
7. Once deployed, go to the resource
8. Navigate to "Keys and Endpoint"
9. Copy:
   - **KEY 1** or **KEY 2**
   - **Endpoint URL**

### 2. Local Setup

1. Install dependencies:
```bash
cd 02-computer-vision/01-Analyze-Images
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your Azure credentials
```

3. Add test images to `data/` folder

4. Run the analysis:
```bash
python src/analyze_images.py
```

## Features Implemented

### Image Analysis Capabilities
- **Caption Generation**: Generate natural language descriptions
- **Dense Captions**: Multiple detailed captions for different image regions
- **Tag Detection**: Identify relevant tags with confidence scores
- **Object Detection**: Locate and identify objects with bounding boxes
- **People Detection**: Detect people and their locations in images

### Supported Image Formats
- JPEG/JPG
- PNG
- BMP
- GIF

### Analysis Output
The script provides:
- Main caption with confidence score
- Dense captions for image regions
- List of tags with confidence scores
- Object locations with bounding boxes
- People count and locations

## Code Structure
```
01-Analyze-Images/
├── src/
│   ├── analyze_images.py     # Main analysis script
│   └── utils.py              # Helper functions
├── data/
│   └── sample_images/        # Test images
├── docs/
│   └── LAB_INSTRUCTIONS.md   # Original lab instructions
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## Sample Usage

```python
from analyze_images import ImageAnalyzer

# Initialize analyzer
analyzer = ImageAnalyzer(endpoint, key)

# Analyze local image
result = analyzer.analyze_local_image("data/street.jpg")

# Analyze image from URL
result = analyzer.analyze_url("https://example.com/image.jpg")
```

## Business Applications
- **E-commerce**: Auto-generate product descriptions
- **Content Moderation**: Detect inappropriate content
- **Accessibility**: Generate alt-text for images
- **Security**: People counting and monitoring
- **Inventory**: Object detection and counting

## Troubleshooting

### Common Issues
1. **401 Unauthorized**: Check your API key
2. **404 Not Found**: Verify endpoint URL
3. **429 Too Many Requests**: Free tier limit reached (20 calls/minute)
4. **Image too large**: Max 4MB for free tier

### Solutions
- Ensure correct region for your resource
- Use supported image formats
- Resize large images before analysis
- Implement retry logic with delays

## Cost Considerations
- **Free Tier (F0)**: 5,000 transactions/month, 20 calls/minute
- **Standard Tier (S1)**: $1 per 1,000 transactions
- **Batch processing**: Consider batching for cost efficiency

## Next Steps
- Implement custom vision models
- Add face detection capabilities
- Integrate with storage for batch processing
- Build web interface for image uploads

## Resources
- [Azure AI Vision Documentation](https://docs.microsoft.com/azure/cognitive-services/computer-vision/)
- [Python SDK Reference](https://docs.microsoft.com/python/api/azure-ai-vision-imageanalysis/)
- [REST API Reference](https://westus.dev.cognitive.microsoft.com/docs/services/computer-vision-v3-2/operations/56f91f2e778daf14a499f21b)

---
*Part of Azure AI Engineer Learning Journey*