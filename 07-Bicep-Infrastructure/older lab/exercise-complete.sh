#!/bin/bash

echo "=== Microsoft Learn Exercise: Bicep Parameters and SQL Database ==="
echo ""
echo "This script will deploy the resources needed for the exercise."
echo "Region: Central US (to avoid East US capacity issues)"
echo ""

# Variables
RG="learn-a1f925d6-2479-4334-8988-141211ac7fb8"
TIMESTAMP=$(date +%Y%m%d%H%M%S)
DEPLOYMENT_NAME="bicep-lab-$TIMESTAMP"

# Show current Azure account
echo "Current Azure subscription:"
az account show --query name -o tsv
echo ""

# Option 1: Try with inline parameters
echo "Attempting deployment with inline parameters..."
az deployment group create \
  --name "$DEPLOYMENT_NAME" \
  --resource-group "$RG" \
  --template-file main.bicep \
  --parameters @main.parameters.dev.json \
  --parameters sqlServerAdministratorLogin='sqladmin' \
  --parameters sqlServerAdministratorPassword='P@ssw0rd123!' \
  2>&1 | grep -v "The content for this response"

# If that fails, show alternative
if [ $? -ne 0 ]; then
    echo ""
    echo "=== Alternative: Deploy via Azure Portal ==="
    echo "1. Go to: https://portal.azure.com"
    echo "2. Navigate to Resource Group: $RG"
    echo "3. Click '+ Create' > 'Template deployment'"
    echo "4. Select 'Build your own template'"
    echo "5. Copy the content from main.bicep"
    echo "6. Use these parameters:"
    echo "   - location: centralus"
    echo "   - environmentName: dev"
    echo "   - appServicePlanSku: {name: 'F1', tier: 'Free'}"
    echo "   - sqlDatabaseSku: {name: 'Basic', tier: 'Basic'}"
    echo "   - sqlServerAdministratorLogin: sqladmin"
    echo "   - sqlServerAdministratorPassword: P@ssw0rd123!"
else
    echo ""
    echo "Deployment initiated successfully!"
    echo "Checking resources..."
    sleep 30
    az resource list --resource-group "$RG" --query "[?contains(name, '$TIMESTAMP')].[name, type]" -o table
fi