# Custom Entity Extraction - Troubleshooting Guide

## Common Issues and Solutions

### 1. Storage Account Access Denied

**Symptoms**:
- Error: "Forbidden: Access to the storage account was denied"
- Cannot create or access custom entity project in Language Studio

**Root Cause**: 
Language resource lacks proper permissions to access the storage account.

**Solution**:
```bash
# 1. Check if managed identity is enabled
az cognitiveservices account identity show \
  --name azurelanguagecuratest \
  --resource-group cog-search-language-exe

# 2. Get the principal ID from output
# Example: "principalId": "b1c48bac-1cd8-4054-b94b-859753173674"

# 3. Assign Storage Blob Data Owner role
az role assignment create \
  --assignee b1c48bac-1cd8-4054-b94b-859753173674 \
  --role "Storage Blob Data Owner" \
  --scope "/subscriptions/b383d2e9-ed64-4dcd-93d3-e7352ddd7091/resourceGroups/cog-search-language-exe/providers/Microsoft.Storage/storageAccounts/acs118245curastr"
```

### 2. CORS Configuration Error

**Symptoms**:
- Error: "Cannot destructure property 'blobs' of '(intermediate value)' as it is undefined"
- Error: "Make sure your CORS is configured correctly on your storage resource"
- Project creates but cannot access blobs/files

**Root Cause**: 
Browser security (CORS) prevents Language Studio from accessing storage account.

**Solution**:
```bash
# 1. Get storage account key
STORAGE_KEY=$(az storage account keys list \
  --account-name acs118245curastr \
  --resource-group cog-search-language-exe \
  --query "[0].value" -o tsv)

# 2. Configure CORS
az storage cors add \
  --services b \
  --methods GET POST PUT DELETE OPTIONS HEAD \
  --origins "*" \
  --allowed-headers "*" \
  --exposed-headers "*" \
  --max-age 3600 \
  --account-name acs118245curastr \
  --account-key "$STORAGE_KEY"

# 3. Verify CORS settings
az storage cors list \
  --services b \
  --account-name acs118245curastr \
  --account-key "$STORAGE_KEY" \
  -o table
```

**Post-Fix Actions**:
1. Hard refresh browser (Ctrl+F5 or Cmd+Shift+R)
2. Clear browser cache if needed
3. Try incognito/private window

### 3. Understanding the Two-Layer Security

**Why both fixes are needed**:

1. **Azure-level security (Role Assignment)**:
   - Controls service-to-service authentication
   - Allows Language resource to access Storage programmatically
   - Like giving someone a key to your house

2. **Browser-level security (CORS)**:
   - Controls web browser access
   - Allows Language Studio UI to fetch storage data
   - Like telling security it's OK for the keyholder to enter

### 4. Quick Diagnostic Commands

```bash
# Check all role assignments for storage
az role assignment list \
  --scope "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage>" \
  --query "[?principalType=='ServicePrincipal'].{role:roleDefinitionName, assignee:principalId}" \
  -o table

# Check storage container access
az storage container list \
  --account-name <storage-name> \
  --account-key "<key>" \
  --query "[].name" \
  -o tsv

# Test blob access
az storage blob list \
  --container-name classifieds \
  --account-name <storage-name> \
  --account-key "<key>" \
  --query "[].name" \
  -o tsv
```

## Prevention Tips

1. **When creating Language resource**: Enable managed identity during creation
2. **When creating storage**: Consider CORS requirements upfront
3. **Use Azure Portal**: Sometimes easier for initial setup, then CLI for automation

## Resources
- [Language Service Storage Requirements](https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/custom-named-entity-recognition/how-to/create-project)
- [CORS in Azure Storage](https://docs.microsoft.com/en-us/rest/api/storageservices/cross-origin-resource-sharing--cors--support-for-the-azure-storage-services)