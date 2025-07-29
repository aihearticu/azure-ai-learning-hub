// Exercise 3: Refactor using Bicep Modules
// This exercise demonstrates how to break down a monolithic template into reusable modules

// Parameters remain in the main template
param location string = 'eastus'
param storageAccountName string = 'toylaunch${uniqueString(resourceGroup().id)}'
param appServiceAppName string = 'toylaunch${uniqueString(resourceGroup().id)}'

@allowed([
  'nonprod'
  'prod'
])
param environmentType string

// Storage-related logic stays in main template (for now)
var storageAccountSkuName = (environmentType == 'prod') ? 'Standard_GRS' : 'Standard_LRS'

// Storage Account resource - could also be moved to a module
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: storageAccountSkuName
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
  }
}

// App Service resources are now in a module
module appService 'modules/appService.bicep' = {
  name: 'appService'
  params: {
    location: location
    appServiceAppName: appServiceAppName
    environmentType: environmentType
  }
}

// Outputs
output storageAccountName string = storageAccount.name
output appServiceAppHostName string = appService.outputs.appServiceAppHostName