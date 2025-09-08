#!/bin/bash

# Comprehensive Azure AI Services Container Test Suite
# This script runs all available tests and provides a summary

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Azure AI Services Container - Comprehensive Test Suite   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found. Creating from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}Please edit .env with your Azure credentials before running tests.${NC}"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Function to check if container is running
check_container() {
    if docker ps | grep -q "azure-ai-language"; then
        echo -e "${GREEN}✓ Container is running${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ Container is not running. Starting container...${NC}"
        bash scripts/deploy-container.sh
        sleep 5
        return 1
    fi
}

# Function to run a test with timing
run_test() {
    local test_name=$1
    local test_script=$2
    
    echo -e "\n${YELLOW}▶ Running: $test_name${NC}"
    echo "────────────────────────────────────────────"
    
    start_time=$(date +%s)
    
    if python3 $test_script; then
        echo -e "${GREEN}✓ $test_name completed successfully${NC}"
    else
        echo -e "${RED}✗ $test_name failed${NC}"
    fi
    
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo -e "${BLUE}Duration: ${duration} seconds${NC}"
}

# Main execution
echo -e "\n${YELLOW}Step 1: Environment Check${NC}"
echo "────────────────────────────────────────────"
echo "Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python3 installed:${NC} $(python3 --version)"
else
    echo -e "${RED}✗ Python3 not found${NC}"
    exit 1
fi

# Check Docker
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Docker installed:${NC} $(docker --version)"
else
    echo -e "${RED}✗ Docker not found${NC}"
    exit 1
fi

# Check Azure CLI
if command -v az &> /dev/null; then
    echo -e "${GREEN}✓ Azure CLI installed:${NC} $(az --version | head -1)"
else
    echo -e "${YELLOW}⚠ Azure CLI not found (optional)${NC}"
fi

# Install Python dependencies
echo -e "\n${YELLOW}Step 2: Installing Python Dependencies${NC}"
echo "────────────────────────────────────────────"
pip install -q requests python-dotenv

# Check container status
echo -e "\n${YELLOW}Step 3: Container Status${NC}"
echo "────────────────────────────────────────────"
check_container

# Wait for container to be ready
echo -e "\n${YELLOW}Waiting for container to be ready...${NC}"
sleep 3

# Run all tests
echo -e "\n${BLUE}════════════════════════════════════════════${NC}"
echo -e "${BLUE}          RUNNING TEST SUITE${NC}"
echo -e "${BLUE}════════════════════════════════════════════${NC}"

# Make scripts executable
chmod +x scripts/*.py

# Test 1: Language Detection
run_test "Language Detection Test" "scripts/test-language-detection.py"

# Test 2: Sentiment Analysis
run_test "Sentiment Analysis Test" "scripts/test-sentiment-analysis.py"

# Test 3: Key Phrase Extraction
run_test "Key Phrase Extraction Test" "scripts/test-key-phrases.py"

# Test 4: Entity Recognition
run_test "Named Entity Recognition Test" "scripts/test-entity-recognition.py"

# Summary
echo -e "\n${BLUE}════════════════════════════════════════════${NC}"
echo -e "${BLUE}              TEST SUMMARY${NC}"
echo -e "${BLUE}════════════════════════════════════════════${NC}"

echo -e "\n${GREEN}All tests completed!${NC}"

echo -e "\n${YELLOW}Container Information:${NC}"
docker ps --filter "name=azure-ai-language" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo -e "\n${YELLOW}Available Endpoints:${NC}"
echo "• Health Check: http://localhost:5000/health"
echo "• Language Detection: http://localhost:5000/text/analytics/v3.1/languages"
echo "• Sentiment Analysis: http://localhost:5000/text/analytics/v3.1/sentiment"
echo "• Key Phrases: http://localhost:5000/text/analytics/v3.1/keyPhrases"
echo "• Entity Recognition: http://localhost:5000/text/analytics/v3.1/entities/recognition/general"
echo "• PII Detection: http://localhost:5000/text/analytics/v3.1/entities/recognition/pii"

echo -e "\n${YELLOW}Useful Docker Commands:${NC}"
echo "• View logs: docker logs azure-ai-language"
echo "• Stop container: docker stop azure-ai-language"
echo "• Remove container: docker rm azure-ai-language"
echo "• Check resource usage: docker stats azure-ai-language"

echo -e "\n${GREEN}✓ Test suite execution complete!${NC}"