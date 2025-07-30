# Bicep Troubleshooting Guide

## Common Issues and Solutions

### 1. Storage Account Name Already Exists
**Error**: `StorageAccountAlreadyTaken`

**Solution**: 
- Storage account names must be globally unique
- Use `uniqueString()` function with resource group ID
- Alternatively, add a unique suffix to the parameter

### 2. Invalid SKU for Region
**Error**: `SkuNotAvailable`

**Solution**:
- Check available SKUs in your region: `az vm list-skus --location eastus`
- Some SKUs (like P2v3) may not be available in all regions
- Use F1 (free tier) for development

### 3. Module Not Found
**Error**: `Unable to load module`

**Solution**:
- Ensure the module path is relative to the main template
- Check that the module file exists at the specified path
- Use forward slashes (/) in paths, even on Windows

### 4. Parameter Type Mismatch
**Error**: `The parameter 'environmentType' expects a value of type 'String'`

**Solution**:
- Ensure you're passing the correct parameter type
- Use allowed values: 'nonprod' or 'prod'
- Check for typos in parameter names

### 5. Deployment What-If Issues
**Command**: `az deployment group what-if`

**Solution**:
- Use `--template-file` not `--template`
- Ensure all required parameters are provided
- Add `--parameters` before each parameter

## Useful Commands

### Validate Template
```bash
az deployment group validate \
  --resource-group myRG \
  --template-file main.bicep
```

### Debug Deployment
```bash
az deployment group create \
  --resource-group myRG \
  --template-file main.bicep \
  --parameters environmentType=nonprod \
  --debug
```

### List Recent Deployments
```bash
az deployment group list \
  --resource-group myRG \
  --output table
```

### View Deployment Operations
```bash
az deployment operation group list \
  --resource-group myRG \
  --name deploymentName
```