#!/bin/bash

echo "Starting Bicep deployment for SQL Database exercise..."
echo "This will deploy to West US 2 region"
echo ""

# Set variables
RG="learn-a1f925d6-2479-4334-8988-141211ac7fb8"
DEPLOYMENT_NAME="sql-bicep-$(date +%Y%m%d%H%M%S)"
LOCATION="westus2"

# Show what we're deploying
echo "Deployment details:"
echo "- Resource Group: $RG"
echo "- Deployment Name: $DEPLOYMENT_NAME"
echo "- Location: $LOCATION"
echo ""

# Run the deployment
echo "Running deployment..."
az deployment group create \
  --name "$DEPLOYMENT_NAME" \
  --resource-group "$RG" \
  --template-file main.bicep \
  --parameters @main.parameters.dev.json \
  --parameters sqlServerAdministratorLogin="sqladmin" \
  --parameters sqlServerAdministratorPassword="P@ssw0rd123!" \
  --parameters location="$LOCATION" \
  --verbose

# Check result
if [ $? -eq 0 ]; then
    echo "Deployment completed successfully!"
    echo "Checking deployed resources..."
    az resource list --resource-group "$RG" --query "[?contains(name, 'sql')].[name, type]" -o table
else
    echo "Deployment failed. Checking logs..."
    az deployment operation group list --resource-group "$RG" --name "$DEPLOYMENT_NAME" --query "[?properties.provisioningState=='Failed']" -o json
fi