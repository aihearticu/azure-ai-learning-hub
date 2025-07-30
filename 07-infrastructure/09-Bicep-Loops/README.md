# Bicep Loops Exercise

## Overview
This module demonstrates how to use loops in Azure Bicep to deploy multiple resources based on array parameters. We implemented a multi-region deployment including databases, virtual networks, and enhanced output loops.

## Learning Objectives
- Use array parameters to define multiple deployment configurations
- Implement copy loops with the `for` expression
- Deploy resources to multiple Azure regions
- Use variable loops to transform parameter data
- Create complex output loops with object structures
- Deploy virtual networks with dynamic subnet configuration

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

### 3. Variable Loops
```bicep
var subnetProperties = [for subnet in subnets: {
  name: subnet.name
  properties: {
    addressPrefix: subnet.ipAddressRange
  }
}]
```

### 4. Resource Loops
```bicep
resource virtualNetworks 'Microsoft.Network/virtualNetworks@2024-05-01' = [for location in locations: {
  name: 'teddybear-${location}'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [virtualNetworkAddressPrefix]
    }
    subnets: subnetProperties
  }
}]
```

### 5. Complex Output Loops
```bicep
output serverInfo array = [for i in range(0, length(locations)): {
  name: databases[i].outputs.serverName
  location: databases[i].outputs.location
  fullyQualifiedDomainName: databases[i].outputs.serverFullyQualifiedDomainName
}]
```

## Implementation Details

### Files Created
1. **main-loops.bicep** - Main template with 3 regions (westus, eastus2, westeurope)
2. **main-loops-small.bicep** - Reduced to 2 regions to avoid subscription limits
3. **modules/database.bicep** - Modularized database deployment logic

### Key Features
- Deploys SQL servers and databases to multiple regions
- Creates virtual networks with frontend and backend subnets
- Uses unique naming convention: `teddy${location}${uniqueString}`
- Conditional audit storage accounts (Production only)
- Modular design for reusability
- Enhanced outputs with fully qualified domain names

## Deployment Results
Successfully deployed:

### SQL Servers
- **West US**: teddywestuslzng4pw7iumfa.database.windows.net
- **East US 2**: teddyeastus2lzng4pw7iumfa.database.windows.net

### Virtual Networks
- **West US**: teddybear-westus (10.10.0.0/16)
  - Frontend subnet: 10.10.5.0/24
  - Backend subnet: 10.10.10.0/24
- **East US 2**: teddybear-eastus2 (10.10.0.0/16)
  - Frontend subnet: 10.10.5.0/24
  - Backend subnet: 10.10.10.0/24

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

## Exercise Progression

### Exercise 1: Basic Loops
- Deploy resources to multiple regions
- Use module loops for consistency

### Exercise 2: Variable Loops
- Transform parameter arrays into resource properties
- Deploy virtual networks with dynamic subnets

### Exercise 3: Output Loops
- Create complex output structures
- Include computed properties like FQDNs

## Next Steps
- Experiment with more complex loop scenarios
- Combine loops with conditions for advanced deployments
- Use loops for deploying different resource types
- Explore nested loops for multi-dimensional deployments

## Reference
[Microsoft Learn - Build flexible Bicep templates by using conditions and loops](https://learn.microsoft.com/en-us/training/modules/build-flexible-bicep-files-conditions-loops/)