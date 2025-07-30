# Bicep Modules Exercise

## Overview
This module demonstrates how to create reusable Bicep modules for common deployment patterns. We built a modular solution for deploying a web application with optional CDN.

## Learning Objectives
- Create reusable Bicep modules
- Use modules in parent templates
- Pass parameters between modules
- Implement conditional module deployment
- Access module outputs

## Module Architecture

```
main.bicep
├── modules/app.bicep    (App Service + Plan)
└── modules/cdn.bicep    (CDN Profile + Endpoint)
```

## Key Concepts

### 1. Creating a Module
Modules are just Bicep files that define reusable resources:
```bicep
// modules/app.bicep
param location string
param appServiceAppName string

resource appServiceApp 'Microsoft.Web/sites@2024-04-01' = {
  name: appServiceAppName
  location: location
  // ...
}

output appServiceAppHostName string = appServiceApp.properties.defaultHostName
```

### 2. Using a Module
Reference modules in your main template:
```bicep
module app 'modules/app.bicep' = {
  name: 'website'  // Deployment name
  params: {
    location: location
    appServiceAppName: appServiceAppName
  }
}
```

### 3. Conditional Module Deployment
Deploy modules based on conditions:
```bicep
module cdn 'modules/cdn.bicep' = if (deployCdn) {
  name: 'cdn'
  params: {
    originHostName: app.outputs.appServiceAppHostName
  }
}
```

### 4. Module Dependencies
Modules can depend on outputs from other modules:
```bicep
// CDN module uses the App Service hostname
originHostName: app.outputs.appServiceAppHostName
```

## Implementation Details

### Modules Created

1. **app.bicep** - App Service module
   - Creates App Service Plan
   - Creates App Service Web App
   - Outputs the app's hostname

2. **cdn.bicep** - CDN module
   - Creates CDN Profile
   - Creates CDN Endpoint
   - Configures origin from App Service
   - Outputs the CDN endpoint hostname

3. **main.bicep** - Parent template
   - Uses both modules
   - Implements conditional CDN deployment
   - Aggregates outputs

## Deployment Results

### With CDN Enabled
```bash
✅ App Service: toy-lzng4pw7iumfa.azurewebsites.net
✅ CDN Endpoint: endpoint-lzng4pw7iumfa.azureedge.net
```

### Without CDN
```bash
✅ App Service: toy-lzng4pw7iumfa.azurewebsites.net
❌ CDN Endpoint: (not deployed)
```

## Benefits of Modularization

1. **Reusability**: Modules can be used across multiple deployments
2. **Maintainability**: Changes in one place affect all uses
3. **Testing**: Modules can be tested independently
4. **Separation of Concerns**: Each module has a specific purpose
5. **Team Collaboration**: Different teams can own different modules

## Commands Used

```bash
# Deploy with CDN
az deployment group create \
  --resource-group "learn-fdf762cf-22b3-4660-aa29-7b1127520968" \
  --template-file main.bicep \
  --parameters appServicePlanSkuName=F1 deployCdn=true

# Deploy without CDN
az deployment group create \
  --resource-group "learn-fdf762cf-22b3-4660-aa29-7b1127520968" \
  --template-file main.bicep \
  --parameters appServicePlanSkuName=F1 deployCdn=false
```

## Best Practices

1. **Module Naming**: Use descriptive names that indicate purpose
2. **Parameter Validation**: Add constraints and descriptions
3. **Output Everything Needed**: Modules should output values that consumers might need
4. **Keep Modules Focused**: One module = one logical component
5. **Version Control**: Track module versions for stability

## Common Patterns

### Pattern 1: Resource + Configuration
```bicep
module database 'modules/database.bicep' = {
  name: 'database'
  params: {
    // Resource parameters
  }
}

module databaseConfig 'modules/database-config.bicep' = {
  name: 'database-config'
  params: {
    databaseName: database.outputs.name
    // Configuration parameters
  }
}
```

### Pattern 2: Environment-Specific Modules
```bicep
module prodResources 'modules/production.bicep' = if (environment == 'Production') {
  name: 'prod-resources'
  params: {
    // Production-specific resources
  }
}
```

## Next Steps
- Create modules for your common patterns
- Build a module library for your organization
- Implement module versioning
- Create nested module hierarchies

## Reference
[Microsoft Learn - Create composable Bicep files by using modules](https://learn.microsoft.com/en-us/training/modules/create-composable-bicep-files-using-modules/)