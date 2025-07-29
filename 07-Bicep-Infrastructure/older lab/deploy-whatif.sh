#!/bin/bash

# Test deployment with What-If first
RG="learn-a1f925d6-2479-4334-8988-141211ac7fb8"

echo "Running What-If analysis first..."

# Create a temporary parameters file with all values
cat > temp-params.json << 'EOF'
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "location": {
      "value": "westus2"
    },
    "appServicePlanSku": {
      "value": {
        "name": "F1",
        "tier": "Free"
      }
    },
    "sqlDatabaseSku": {
      "value": {
        "name": "Standard",
        "tier": "Standard"
      }
    },
    "sqlServerAdministratorLogin": {
      "value": "sqladmin"
    },
    "sqlServerAdministratorPassword": {
      "value": "P@ssw0rd123!"
    }
  }
}
EOF

# Run What-If
echo "Checking what will be deployed..."
az deployment group what-if \
  --resource-group "$RG" \
  --template-file main.bicep \
  --parameters @temp-params.json

# Ask for confirmation
read -p "Do you want to proceed with deployment? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Deploying..."
    az deployment group create \
      --name "sql-deploy-final" \
      --resource-group "$RG" \
      --template-file main.bicep \
      --parameters @temp-params.json
fi

# Clean up
rm -f temp-params.json