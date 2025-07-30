#!/bin/bash

# Explicit deployment with all parameters
DEPLOYMENT_NAME="sql-deploy-$(date +%s)"
RG="learn-a1f925d6-2479-4334-8988-141211ac7fb8"

echo "Deploying with explicit parameters..."
echo "Deployment name: $DEPLOYMENT_NAME"
echo "Resource group: $RG"
echo "Location: westus2"

# Deploy with all parameters explicitly set
az deployment group create \
  --name "$DEPLOYMENT_NAME" \
  --resource-group "$RG" \
  --template-file main.bicep \
  --parameters appServicePlanSku='{"name":"F1","tier":"Free"}' \
  --parameters sqlDatabaseSku='{"name":"Standard","tier":"Standard"}' \
  --parameters sqlServerAdministratorLogin="sqladmin" \
  --parameters sqlServerAdministratorPassword="P@ssw0rd123!" \
  --parameters location="westus2"

echo "Checking deployment status..."
az deployment group show \
  --name "$DEPLOYMENT_NAME" \
  --resource-group "$RG" \
  --query "properties.provisioningState" \
  -o tsv