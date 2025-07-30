#!/bin/bash

# Deploy to Central US with all parameters
export AZURE_CORE_NO_COLOR=true
export DEPLOYMENT_NAME="lab-exercise-$(date +%s)"
export RG="learn-a1f925d6-2479-4334-8988-141211ac7fb8"

echo "Deploying Bicep template to Central US..."
echo "Deployment name: $DEPLOYMENT_NAME"

# Create a complete parameter file for this deployment
cat > deploy-params.json << 'EOF'
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "location": {
      "value": "centralus"
    },
    "environmentName": {
      "value": "dev"
    },
    "appServicePlanSku": {
      "value": {
        "name": "F1",
        "tier": "Free"
      }
    },
    "sqlDatabaseSku": {
      "value": {
        "name": "Basic",
        "tier": "Basic"
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

# Deploy
az deployment group create \
  --name "$DEPLOYMENT_NAME" \
  --resource-group "$RG" \
  --template-file main.bicep \
  --parameters @deploy-params.json \
  --only-show-errors

# Check deployment status
echo ""
echo "Checking deployment status..."
az deployment group show \
  --name "$DEPLOYMENT_NAME" \
  --resource-group "$RG" \
  --query "{status:properties.provisioningState, timestamp:properties.timestamp}" \
  -o table

# Clean up temp file
rm -f deploy-params.json