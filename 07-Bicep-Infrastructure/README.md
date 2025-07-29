# Module 07: Build Your First Bicep File

## Overview
This module covers the fundamentals of Azure Bicep, an Infrastructure as Code (IaC) language for declaratively deploying Azure resources.

**Microsoft Learn Module**: [Build your first Bicep file](https://learn.microsoft.com/en-us/training/modules/build-first-bicep-file/)

## Learning Objectives
- Understand Bicep syntax and structure
- Deploy Azure resources using Bicep
- Use parameters and variables for flexible deployments
- Implement environment-specific configurations

## Module Structure

```
07-Bicep-Infrastructure/
├── README.md                          # This file
├── src/
│   ├── main.bicep                    # Initial hardcoded version
│   ├── main-with-params.bicep        # Version with parameters and variables
│   └── main-modular.bicep            # Modular version (future exercise)
├── exercises/
│   ├── 01-basic-resources.bicep     # Exercise 1: Basic resource deployment
│   ├── 02-parameters-variables.bicep # Exercise 2: Add parameters and variables
│   └── 03-conditions-loops.bicep    # Exercise 3: Advanced features
├── deployments/
│   ├── deploy-dev.sh                 # Development deployment script
│   └── deploy-prod.sh                # Production deployment script
└── docs/
    ├── key-concepts.md               # Key Bicep concepts
    └── troubleshooting.md            # Common issues and solutions
```

## Key Concepts Covered

### 1. Basic Bicep Syntax
- Resource declarations
- API versions
- Resource properties

### 2. Parameters
- Input parameters for flexible deployments
- Parameter decorators (@allowed, @description)
- Default values

### 3. Variables
- Computed values
- Conditional logic with ternary operators
- Environment-specific configurations

### 4. Functions
- `uniqueString()` - Generate unique names
- `resourceGroup()` - Access resource group properties
- String manipulation functions

## Exercise Progress

### Exercise 1: Basic Resources ✅
Created initial Bicep file with:
- Storage Account
- App Service Plan
- App Service Web App

### Exercise 2: Parameters and Variables ✅
Enhanced with:
- Location parameter
- Dynamic naming with `uniqueString()`
- Environment type parameter (prod/nonprod)
- Conditional SKU selection

### Exercise 3: Advanced Features (Upcoming)
Will cover:
- Modules
- Loops
- Outputs
- Dependencies

## Deployment Commands

### Deploy to Development
```bash
az deployment group create \
  --name main-dev \
  --template-file src/main-with-params.bicep \
  --parameters environmentType=nonprod
```

### Deploy to Production
```bash
az deployment group create \
  --name main-prod \
  --template-file src/main-with-params.bicep \
  --parameters environmentType=prod
```

## Key Learnings

1. **Infrastructure as Code Benefits**
   - Version control for infrastructure
   - Repeatable deployments
   - Environment parity

2. **Bicep vs ARM Templates**
   - Cleaner syntax
   - Better tooling support
   - Automatic dependency management

3. **Best Practices**
   - Use parameters for environment-specific values
   - Leverage `uniqueString()` for globally unique names
   - Separate concerns with modules
   - Use variables for computed values

## Resources
- [Bicep Documentation](https://docs.microsoft.com/azure/azure-resource-manager/bicep/)
- [Bicep Playground](https://bicepdemo.z22.web.core.windows.net/)
- [Azure Resource Reference](https://docs.microsoft.com/azure/templates/)

## Next Steps
- Complete Module 8: [Build reusable Bicep templates by using parameters](https://learn.microsoft.com/training/modules/build-reusable-bicep-templates-parameters/)
- Explore Bicep modules and advanced patterns