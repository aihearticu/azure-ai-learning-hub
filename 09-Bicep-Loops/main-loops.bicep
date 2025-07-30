@description('The Azure regions into which the resources should be deployed.')
param locations array = [
  'westus'
  'eastus2'
  'westeurope'
]

@secure()
@description('The administrator login username for the SQL server.')
param sqlServerAdministratorLogin string

@secure()
@description('The administrator login password for the SQL server.')
param sqlServerAdministratorLoginPassword string

@description('The name and tier of the SQL database SKU.')
param sqlDatabaseSku object = {
  name: 'Standard'
  tier: 'Standard'
}

@description('The name of the environment. This must be Development or Production.')
@allowed([
  'Development'
  'Production'
])
param environmentName string = 'Development'

@description('The name of the audit storage account SKU.')
param auditStorageAccountSkuName string = 'Standard_LRS'

@description('The address prefix for the virtual network')
param virtualNetworkAddressPrefix string = '10.10.0.0/16'

@description('The subnet configuration for the virtual network')
param subnets array = [
  {
    name: 'frontend'
    ipAddressRange: '10.10.5.0/24'
  }
  {
    name: 'backend'
    ipAddressRange: '10.10.10.0/24'
  }
]

var subnetProperties = [for subnet in subnets: {
  name: subnet.name
  properties: {
    addressPrefix: subnet.ipAddressRange
  }
}]

module databases 'modules/database.bicep' = [for location in locations: {
  name: 'database-${location}'
  params: {
    location: location
    sqlServerAdministratorLogin: sqlServerAdministratorLogin
    sqlServerAdministratorLoginPassword: sqlServerAdministratorLoginPassword
    sqlDatabaseSku: sqlDatabaseSku
    environmentName: environmentName
    auditStorageAccountSkuName: auditStorageAccountSkuName
  }
}]

resource virtualNetworks 'Microsoft.Network/virtualNetworks@2024-05-01' = [for location in locations: {
  name: 'teddybear-${location}'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        virtualNetworkAddressPrefix
      ]
    }
    subnets: subnetProperties
  }
}]

output serverNames array = [for i in range(0, length(locations)): databases[i].outputs.serverName]
output databaseNames array = [for i in range(0, length(locations)): databases[i].outputs.databaseName]
output locations array = [for i in range(0, length(locations)): databases[i].outputs.location]

output serverInfo array = [for i in range(0, length(locations)): {
  name: databases[i].outputs.serverName
  location: databases[i].outputs.location
  fullyQualifiedDomainName: databases[i].outputs.serverFullyQualifiedDomainName
}]