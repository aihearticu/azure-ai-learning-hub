#!/bin/bash

# Deploy to production environment
# Usage: ./deploy-prod.sh [resource-group-name]

RESOURCE_GROUP=${1:-"bicep-learning-prod-rg"}
LOCATION="eastus"
DEPLOYMENT_NAME="bicep-prod-$(date +%Y%m%d%H%M%S)"

echo "⚠️  WARNING: Deploying to PRODUCTION environment!"
echo "Resource Group: $RESOURCE_GROUP"
echo "Location: $LOCATION"
echo ""
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Deployment cancelled."
    exit 1
fi

# Create resource group if it doesn't exist
az group create --name $RESOURCE_GROUP --location $LOCATION 2>/dev/null

# Validate the template first
echo "Validating template..."
az deployment group validate \
  --resource-group $RESOURCE_GROUP \
  --template-file ../src/main-modular.bicep \
  --parameters environmentType=prod \
  --parameters location=$LOCATION

if [ $? -ne 0 ]; then
    echo "Template validation failed!"
    exit 1
fi

# Deploy the Bicep template
echo "Deploying to production..."
az deployment group create \
  --name $DEPLOYMENT_NAME \
  --resource-group $RESOURCE_GROUP \
  --template-file ../src/main-modular.bicep \
  --parameters environmentType=prod \
  --parameters location=$LOCATION \
  --confirm-with-what-if

echo "Production deployment complete!"