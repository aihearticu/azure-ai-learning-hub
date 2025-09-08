#!/bin/bash

# Azure AI Services Container Deployment Script
# This script deploys and configures Azure AI Services in a container

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Azure AI Services Container Deployment${NC}"
echo "========================================"

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo -e "${RED}Error: .env file not found. Please copy .env.example to .env and fill in your values.${NC}"
    exit 1
fi

# Set defaults if not provided
RESOURCE_GROUP=${RESOURCE_GROUP:-"ai-container-lab-rg"}
LOCATION=${LOCATION:-"eastus"}
COGNITIVE_SERVICES_NAME=${COGNITIVE_SERVICES_NAME:-"ai-container-lab-cs"}
CONTAINER_NAME=${CONTAINER_NAME:-"azure-ai-language"}
CONTAINER_PORT=${CONTAINER_PORT:-5000}
HOST_PORT=${HOST_PORT:-5000}

echo -e "${YELLOW}Step 1: Creating Resource Group${NC}"
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION \
    --output table

echo -e "${YELLOW}Step 2: Creating Cognitive Services Account${NC}"
az cognitiveservices account create \
    --name $COGNITIVE_SERVICES_NAME \
    --resource-group $RESOURCE_GROUP \
    --kind TextAnalytics \
    --sku S \
    --location $LOCATION \
    --yes \
    --output table

echo -e "${YELLOW}Step 3: Getting API Key and Endpoint${NC}"
KEY=$(az cognitiveservices account keys list \
    --name $COGNITIVE_SERVICES_NAME \
    --resource-group $RESOURCE_GROUP \
    --query "key1" \
    --output tsv)

ENDPOINT=$(az cognitiveservices account show \
    --name $COGNITIVE_SERVICES_NAME \
    --resource-group $RESOURCE_GROUP \
    --query "properties.endpoint" \
    --output tsv)

echo "API Key: ${KEY:0:10}..." # Show only first 10 characters for security
echo "Endpoint: $ENDPOINT"

# Update .env with actual values
sed -i "s|AZURE_COGNITIVE_SERVICES_KEY=.*|AZURE_COGNITIVE_SERVICES_KEY=$KEY|" .env
sed -i "s|AZURE_COGNITIVE_SERVICES_ENDPOINT=.*|AZURE_COGNITIVE_SERVICES_ENDPOINT=$ENDPOINT|" .env

echo -e "${YELLOW}Step 4: Checking Docker Installation${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

docker --version

echo -e "${YELLOW}Step 5: Pulling Azure AI Language Container${NC}"
# Note: You need to request access to container images
# Visit: https://aka.ms/csgate
docker pull mcr.microsoft.com/azure-cognitive-services/textanalytics/language:latest

echo -e "${YELLOW}Step 6: Running the Container${NC}"
docker run -d \
    --name $CONTAINER_NAME \
    -p $HOST_PORT:$CONTAINER_PORT \
    -e Eula=accept \
    -e Billing=$ENDPOINT \
    -e ApiKey=$KEY \
    mcr.microsoft.com/azure-cognitive-services/textanalytics/language:latest

echo -e "${GREEN}Container deployed successfully!${NC}"
echo "Container Name: $CONTAINER_NAME"
echo "Access the service at: http://localhost:$HOST_PORT"
echo ""
echo "To check container status: docker ps"
echo "To view logs: docker logs $CONTAINER_NAME"
echo "To stop container: docker stop $CONTAINER_NAME"
echo "To remove container: docker rm $CONTAINER_NAME"