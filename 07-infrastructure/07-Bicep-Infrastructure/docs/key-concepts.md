# Bicep Key Concepts

## Parameters
Parameters allow you to customize deployments without modifying the template.

```bicep
param location string = 'eastus'
param environmentType string
```

### Parameter Decorators
- `@allowed()` - Restrict values to a specific list
- `@description()` - Add documentation
- `@minLength()/@maxLength()` - String length constraints
- `@minValue()/@maxValue()` - Numeric constraints

## Variables
Variables store computed values that can be reused.

```bicep
var storageAccountSkuName = (environmentType == 'prod') ? 'Standard_GRS' : 'Standard_LRS'
```

## Functions
Common Bicep functions:
- `uniqueString()` - Generate deterministic unique strings
- `resourceGroup()` - Access resource group properties
- `concat()` - Concatenate strings
- `toLower()/toUpper()` - Change case

## Resource References
Reference other resources using symbolic names:

```bicep
serverFarmId: appServicePlan.id
```

## Conditional Deployments
Deploy resources conditionally:

```bicep
resource exampleResource 'Microsoft.Example/resource@2021-01-01' = if (deployResource) {
  // resource properties
}
```