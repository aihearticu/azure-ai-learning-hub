#!/bin/bash

# Deploy following the Microsoft Learn exercise pattern
# You'll be prompted for the secure parameters

echo "Deploying Bicep template with parameter file..."
echo "You will be prompted for SQL credentials"
echo ""

az deployment group create \
  --template-file main.bicep \
  --parameters main.parameters.dev.json

# Note: Azure CLI will prompt you for:
# - sqlServerAdministratorLogin
# - sqlServerAdministratorPassword