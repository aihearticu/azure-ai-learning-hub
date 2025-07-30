# Lab 05: Extract Custom Entities

This folder contains the work completed for the Microsoft Learn module: [Extract custom entities](https://microsoftlearning.github.io/mslearn-ai-language/Instructions/Labs/05-extract-custom-entities.html)

## Overview
Custom Named Entity Recognition (NER) to identify and extract specific entities from classified ads:
- **ItemForSale**: What's being sold
- **Price**: Cost of the item
- **Location**: Where the item is located

## Lab Components
- Azure AI Language resource configuration
- Custom entity recognition project setup
- Training data labeling
- Model training and deployment
- Client application implementation

## Technologies Used
- Azure AI Language Service
- Azure Language Studio
- Python/Azure SDK

## Troubleshooting Guide

### Issue 1: Storage Account Access Denied
**Error**: "Forbidden: Access to the storage account was denied. The Language resource must have at least 'Storage Blob Data Owner' access"

**Solution**:
1. Enable managed identity on Language resource:
   ```bash
   az cognitiveservices account identity show --name <language-resource> --resource-group <rg-name>
   ```

2. Assign Storage Blob Data Owner role:
   ```bash
   az role assignment create \
     --assignee <managed-identity-id> \
     --role "Storage Blob Data Owner" \
     --scope "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage-name>"
   ```

### Issue 2: CORS Configuration Error
**Error**: "Cannot destructure property 'blobs' of '(intermediate value)' as it is undefined" and "Make sure your CORS is configured correctly"

**Solution**:
1. Get storage account key:
   ```bash
   az storage account keys list --account-name <storage-name> --resource-group <rg-name> --query "[0].value" -o tsv
   ```

2. Configure CORS for Language Studio:
   ```bash
   az storage cors add \
     --services b \
     --methods GET POST PUT DELETE OPTIONS HEAD \
     --origins "*" \
     --allowed-headers "*" \
     --exposed-headers "*" \
     --max-age 3600 \
     --account-name <storage-name> \
     --account-key "<key>"
   ```

3. Verify CORS configuration:
   ```bash
   az storage cors list --services b --account-name <storage-name> --account-key "<key>" -o table
   ```

**Note**: After CORS configuration, you may need to hard refresh (Ctrl+F5) or clear browser cache.

## Setup Instructions

### 1. Clone the Microsoft Learn Repository
```bash
cd "/home/jjhpe/Azure AI Engineer/Azure AI Services Container"
rm -rf mslearn-ai-language
git clone https://github.com/microsoftlearning/mslearn-ai-language
```

### 2. Lab Files Location
- **Main lab files**: `mslearn-ai-language/Labfiles/05-custom-entity-recognition/`
- **Sample data**: `mslearn-ai-language/Labfiles/05-custom-entity-recognition/data/ads.zip`
- **Python starter code**: `mslearn-ai-language/Labfiles/05-custom-entity-recognition/Python/`
- **Test files**: `test1.txt` and `test2.txt` for testing the deployed model

## Lab Progress
- ✅ Azure Language resource created
- ✅ Storage account configured with proper permissions
- ✅ CORS issues resolved
- ✅ Custom entity project created in Language Studio
- ✅ Microsoft Learn repository cloned
- ⏳ Data labeling in progress
- ⏳ Model training pending
- ⏳ Client application pending