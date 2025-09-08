#!/bin/bash

# Container Monitoring Script
# Monitors the Azure AI Services container performance and health

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

CONTAINER_NAME=${CONTAINER_NAME:-"azure-ai-language"}

clear
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       Azure AI Services Container Monitor                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"

# Function to check container health
check_health() {
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health)
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✓ Healthy${NC}"
    else
        echo -e "${RED}✗ Unhealthy (HTTP $response)${NC}"
    fi
}

# Function to get container stats
get_container_stats() {
    docker stats $CONTAINER_NAME --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
}

# Function to show recent logs
show_recent_logs() {
    echo -e "\n${YELLOW}Recent Container Logs (last 10 lines):${NC}"
    docker logs $CONTAINER_NAME --tail 10 2>&1 | sed 's/^/  /'
}

# Function to test endpoint response time
test_response_time() {
    local endpoint=$1
    local name=$2
    
    # Simple test payload
    local payload='{"documents":[{"id":"1","text":"Test","language":"en"}]}'
    
    # Measure response time
    response_time=$(curl -s -o /dev/null -w "%{time_total}" \
        -X POST "http://localhost:5000/text/analytics/v3.1/$endpoint" \
        -H "Content-Type: application/json" \
        -H "Ocp-Apim-Subscription-Key: test" \
        -d "$payload" 2>/dev/null)
    
    # Convert to milliseconds
    response_ms=$(echo "$response_time * 1000" | bc 2>/dev/null || echo "N/A")
    
    printf "  %-25s: %s ms\n" "$name" "$response_ms"
}

# Main monitoring loop
while true; do
    clear
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║       Azure AI Services Container Monitor                    ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo -e "$(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    # Check if container is running
    if ! docker ps | grep -q "$CONTAINER_NAME"; then
        echo -e "${RED}✗ Container '$CONTAINER_NAME' is not running${NC}"
        echo -e "${YELLOW}Run './scripts/deploy-container.sh' to start it${NC}"
        exit 1
    fi
    
    # Container Status
    echo -e "${CYAN}Container Status:${NC}"
    echo -e "  Name: $CONTAINER_NAME"
    echo -n "  Health: "
    check_health
    
    uptime=$(docker ps --filter "name=$CONTAINER_NAME" --format "{{.Status}}")
    echo -e "  Uptime: $uptime"
    
    # Resource Usage
    echo -e "\n${CYAN}Resource Usage:${NC}"
    get_container_stats
    
    # Endpoint Response Times
    echo -e "\n${CYAN}Endpoint Response Times:${NC}"
    test_response_time "languages" "Language Detection"
    test_response_time "sentiment" "Sentiment Analysis"
    test_response_time "keyPhrases" "Key Phrase Extraction"
    test_response_time "entities/recognition/general" "Entity Recognition"
    
    # Port Mapping
    echo -e "\n${CYAN}Port Mapping:${NC}"
    docker port $CONTAINER_NAME
    
    # Volume Mounts
    echo -e "\n${CYAN}Volume Mounts:${NC}"
    docker inspect $CONTAINER_NAME --format '{{range .Mounts}}  {{.Type}}: {{.Source}} -> {{.Destination}}{{"\n"}}{{end}}' 2>/dev/null || echo "  None"
    
    # Environment Variables (showing non-sensitive ones)
    echo -e "\n${CYAN}Configuration:${NC}"
    docker inspect $CONTAINER_NAME --format '{{range .Config.Env}}{{if not (contains . "ApiKey")}}  {{.}}{{"\n"}}{{end}}{{end}}' | grep -E "(Eula|Billing)" | head -3
    
    # Show recent logs
    show_recent_logs
    
    echo -e "\n${YELLOW}Press Ctrl+C to exit | Refreshing in 5 seconds...${NC}"
    sleep 5
done