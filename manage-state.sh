#!/bin/bash
# Pulumi Stack State Management Script
# This script helps export and import stack state to/from the repository

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Load AWS credentials
source ~/.zprofile

# Function to export stack state
export_state() {
    echo -e "${GREEN}Exporting stack state...${NC}"
    pulumi stack export --file stack-state-dev.json
    echo -e "${GREEN}✓ Stack state exported to stack-state-dev.json${NC}"
    echo -e "${YELLOW}⚠ Remember to commit this file if you want to save it in Git${NC}"
}

# Function to import stack state
import_state() {
    echo -e "${GREEN}Importing stack state from stack-state-dev.json...${NC}"
    if [ ! -f "stack-state-dev.json" ]; then
        echo -e "${RED}✗ Error: stack-state-dev.json not found${NC}"
        exit 1
    fi
    pulumi stack import --file stack-state-dev.json
    echo -e "${GREEN}✓ Stack state imported successfully${NC}"
}

# Function to show state info
show_info() {
    echo -e "${GREEN}Current stack information:${NC}"
    pulumi stack
    echo ""
    echo -e "${GREEN}Local state file location:${NC}"
    echo "~/.pulumi/stacks/pulumi-demo-v1/dev.json"
    echo ""
    echo -e "${GREEN}Repository state backup:${NC}"
    if [ -f "stack-state-dev.json" ]; then
        echo "stack-state-dev.json ($(ls -lh stack-state-dev.json | awk '{print $5}'))"
    else
        echo "No backup found"
    fi
}

# Main script
case "$1" in
    export)
        export_state
        ;;
    import)
        import_state
        ;;
    info)
        show_info
        ;;
    *)
        echo "Pulumi Stack State Management"
        echo ""
        echo "Usage: $0 {export|import|info}"
        echo ""
        echo "Commands:"
        echo "  export  - Export current stack state to stack-state-dev.json"
        echo "  import  - Import stack state from stack-state-dev.json"
        echo "  info    - Show current stack information"
        echo ""
        exit 1
        ;;
esac
