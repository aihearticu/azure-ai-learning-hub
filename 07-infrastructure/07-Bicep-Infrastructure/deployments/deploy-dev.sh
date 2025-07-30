#!/bin/bash

# Deploy to development environment
# Usage: ./deploy-dev.sh [resource-group-name]

RESOURCE_GROUP=${1:-"bicep-learning-dev-rg"}
LOCATION="eastus"
DEPLOYMENT_NAME="bicep-dev-$(date +%Y%m%d%H%M%S)"

echo "Deploying to Development environment..."
echo "Resource Group: $RESOURCE_GROUP"
echo "Location: $LOCATION"

# Create resource group if it doesn't exist
az group create --name $RESOURCE_GROUP --location $LOCATION 2>/dev/null

# Deploy the Bicep template
az deployment group create \
  --name $DEPLOYMENT_NAME \
  --resource-group $RESOURCE_GROUP \
  --template-file ../src/main-with-params.bicep \
  --parameters environmentType=nonprod \
  --parameters location=$LOCATION

echo "Deployment complete!"