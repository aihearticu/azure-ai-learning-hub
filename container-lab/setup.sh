#!/bin/bash

# Setup script for Azure AI Services Container Lab
# This script prepares the environment for testing

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Azure AI Services Container Lab Setup${NC}"
echo "======================================="

# Check Python
echo -e "${YELLOW}Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python3 found: $(python3 --version)${NC}"
else
    echo -e "${RED}✗ Python3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check Docker
echo -e "${YELLOW}Checking Docker...${NC}"
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Docker found: $(docker --version)${NC}"
else
    echo -e "${RED}✗ Docker not found. Please install Docker${NC}"
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check Azure CLI
echo -e "${YELLOW}Checking Azure CLI...${NC}"
if command -v az &> /dev/null; then
    echo -e "${GREEN}✓ Azure CLI found${NC}"
else
    echo -e "${YELLOW}⚠ Azure CLI not found (optional but recommended)${NC}"
    echo "Install: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash"
fi

# Create .env from template if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file${NC}"
    echo -e "${YELLOW}Please edit .env and add your Azure credentials${NC}"
fi

# Install Python packages
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip3 install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Make scripts executable
echo -e "${YELLOW}Making scripts executable...${NC}"
chmod +x scripts/*.sh
chmod +x scripts/*.py
echo -e "${GREEN}✓ Scripts are executable${NC}"

echo -e "\n${GREEN}Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Azure credentials"
echo "2. Run: ./scripts/deploy-container.sh"
echo "3. Run tests: ./scripts/run-all-tests.sh"
echo "4. Monitor: ./scripts/monitor-container.sh"