@description('The Azure region into which the resources should be deployed.')
param location string = resourceGroup().location

@description('The name of the App Service app.')
param appServiceAppName string = 'toy-${uniqueString(resourceGroup().id)}'

@description('The name of the App Service plan.')
param appServicePlanName string = 'toy-plan'

@description('The name of the App Service plan SKU.')
@allowed([
  'F1'
  'D1'
  'B1'
  'B2'
  'B3'
  'S1'
  'S2'
  'S3'
  'P1'
  'P2'
  'P3'
  'P4'
])
param appServicePlanSkuName string = 'F1'

@description('Indicates whether a CDN should be deployed.')
param deployCdn bool = true

module app 'modules/app.bicep' = {
  name: 'website'
  params: {
    location: location
    appServiceAppName: appServiceAppName
    appServicePlanName: appServicePlanName
    appServicePlanSkuName: appServicePlanSkuName
  }
}

module cdn 'modules/cdn.bicep' = if (deployCdn) {
  name: 'cdn'
  params: {
    httpsOnly: true
    originHostName: app.outputs.appServiceAppHostName
  }
}

@description('The host name of the App Service app.')
output appServiceAppHostName string = app.outputs.appServiceAppHostName

@description('The host name of the CDN endpoint.')
output cdnEndpointHostName string = deployCdn ? cdn.outputs.endpointHostName : ''