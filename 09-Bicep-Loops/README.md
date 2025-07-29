# Bicep Loops Exercise

## Overview
This module demonstrates how to use loops in Azure Bicep to deploy multiple resources based on array parameters. We implemented a multi-region database deployment using Bicep's `for` expression.

## Learning Objectives
- Use array parameters to define multiple deployment configurations
- Implement copy loops with the `for` expression
- Deploy resources to multiple Azure regions
- Output arrays from loop deployments

## Key Concepts

### 1. Array Parameters
```bicep
@description('The Azure regions into which the resources should be deployed.')
param locations array = [
  'westus'
  'eastus2'
]
```

### 2. Module Loops
```bicep
module databases 'modules/database.bicep' = [for location in locations: {
  name: 'database-${location}'
  params: {
    location: location
    // other parameters
  }
}]
```

### 3. Output Arrays
```bicep
output serverNames array = [for i in range(0, length(locations)): databases[i].outputs.serverName]
```

## Implementation Details

### Files Created
1. **main-loops.bicep** - Main template with 3 regions (westus, eastus2, westeurope)
2. **main-loops-small.bicep** - Reduced to 2 regions to avoid subscription limits
3. **modules/database.bicep** - Modularized database deployment logic

### Key Features
- Deploys SQL servers and databases to multiple regions
- Uses unique naming convention: `teddy${location}${uniqueString}`
- Conditional audit storage accounts (Production only)
- Modular design for reusability

## Deployment Results
Successfully deployed:
- **West US**: teddywestuslzng4pw7iumfa
- **East US 2**: teddyeastus2lzng4pw7iumfa

## Challenges & Solutions

### 1. Output Syntax Error
**Issue**: For-expressions cannot be used directly in object properties
```bicep
// This doesn't work
output deploymentInfo object = {
  serverNames: [for i in range(0, length(locations)): databases[i].outputs.serverName]
}
```

**Solution**: Use separate array outputs
```bicep
output serverNames array = [for i in range(0, length(locations)): databases[i].outputs.serverName]
```

### 2. Conditional Resource Warnings
**Issue**: Bicep warnings about null conditional resources
**Solution**: Since the conditional logic ensures resources exist when referenced, warnings can be safely ignored for Development environments

### 3. Region Limits
**Issue**: Subscription may have limits on regions
**Solution**: Created a smaller version with only 2 regions for testing

## Commands Used
```bash
# Deploy the multi-region template
az deployment group create \
  --resource-group "learn-fdf762cf-22b3-4660-aa29-7b1127520968" \
  --template-file main-loops-small.bicep \
  --parameters sqlServerAdministratorLogin=sqladmin \
  --parameters sqlServerAdministratorLoginPassword='P@ssw0rd123!' \
  --parameters environmentName=Development

# Verify deployment
az sql server list \
  --resource-group "learn-fdf762cf-22b3-4660-aa29-7b1127520968" \
  --query "[].{name:name, location:location}" \
  -o table
```

## Next Steps
- Experiment with more complex loop scenarios
- Combine loops with conditions for advanced deployments
- Use loops for deploying different resource types
- Explore nested loops for multi-dimensional deployments

## Reference
[Microsoft Learn - Build flexible Bicep templates by using conditions and loops](https://learn.microsoft.com/en-us/training/modules/build-flexible-bicep-files-conditions-loops/)