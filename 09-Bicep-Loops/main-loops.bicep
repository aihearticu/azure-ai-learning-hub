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

output serverNames array = [for i in range(0, length(locations)): databases[i].outputs.serverName]
output databaseNames array = [for i in range(0, length(locations)): databases[i].outputs.databaseName]
output locations array = [for i in range(0, length(locations)): databases[i].outputs.location]