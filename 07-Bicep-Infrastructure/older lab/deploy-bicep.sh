#!/bin/bash

# Deployment script for Bicep template with SQL Database

RESOURCE_GROUP="learn-a1f925d6-2479-4334-8988-141211ac7fb8"
DEPLOYMENT_NAME="bicep-sql-$(date +%Y%m%d%H%M%S)"

echo "Deploying Bicep template..."
echo "Resource Group: $RESOURCE_GROUP"
echo "Deployment Name: $DEPLOYMENT_NAME"
echo "Location: West US 2"

az deployment group create \
  --name "$DEPLOYMENT_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --template-file main.bicep \
  --parameters @main.parameters.dev.json

echo "Deployment complete!"