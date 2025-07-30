// Exercise 1: Basic Bicep Resources
// This is the starting point - hardcoded values

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'toylaunchstorage123unique' // Note: Storage account names must be globally unique!
  location: 'eastus'
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
  }
}

resource appServicePlan 'Microsoft.Web/serverfarms@2024-04-01' = {
  name: 'toy-product-launch-plan'
  location: 'eastus'
  sku: {
    name: 'F1' // Free tier
  }
}

resource appServiceApp 'Microsoft.Web/sites@2024-04-01' = {
  name: 'toy-product-launch-app-123'
  location: 'eastus'
  properties: {
    serverFarmId: appServicePlan.id // Reference to the app service plan
    httpsOnly: true
  }
}