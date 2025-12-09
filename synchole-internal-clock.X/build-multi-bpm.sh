#!/bin/bash
#
# SYNCHOLE Multi-BPM Firmware Builder
# Generates firmware for multiple BPM values
#

set -e

# Configuration
SOURCE_FILE="din-sync-hub-xc8-fixed_2.c"
PROJECT_DIR="$HOME/repos/synchole/synchole-internal-clock.X"
OUTPUT_DIR="$PROJECT_DIR/bpm-builds"
BPMS=(60 80 90 100 110 120 130 140 150 160 180 200 240)

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}   SYNCHOLE Multi-BPM Firmware Builder${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Backup original source
if [ ! -f "$PROJECT_DIR/${SOURCE_FILE}.original" ]; then
    echo -e "${YELLOW}Backing up original source...${NC}"
    cp "$PROJECT_DIR/$SOURCE_FILE" "$PROJECT_DIR/${SOURCE_FILE}.original"
fi

# Build for each BPM
for BPM in "${BPMS[@]}"; do
    echo -e "\n${GREEN}Building ${BPM} BPM firmware...${NC}"
    
    # Calculate period (60000 / (BPM * 24))
    PERIOD=$(python3 -c "print(int(round(60000 / ($BPM * 24))))")
    echo "  Period: ${PERIOD}ms"
    
    # Modify source file
    cp "$PROJECT_DIR/${SOURCE_FILE}.original" "$PROJECT_DIR/$SOURCE_FILE"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/#define INTERNAL_CLOCK_PERIOD_MS.*/#define INTERNAL_CLOCK_PERIOD_MS $PERIOD  \/\/ ${BPM} BPM/" "$PROJECT_DIR/$SOURCE_FILE"
    else
        # Linux
        sed -i "s/#define INTERNAL_CLOCK_PERIOD_MS.*/#define INTERNAL_CLOCK_PERIOD_MS $PERIOD  \/\/ ${BPM} BPM/" "$PROJECT_DIR/$SOURCE_FILE"
    fi
    
    # Build in MPLAB X (headless)
    cd "$PROJECT_DIR"
    echo "  Compiling..."
    make clean > /dev/null 2>&1
    make > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "  ${GREEN}✓ Compile successful${NC}"
        
        # Convert to SysEx
        echo "  Converting to .syx..."
        ./hextosyx.py b dist/default/production/*.hex "$OUTPUT_DIR/synchole-${BPM}bpm.syx" > /dev/null 2>&1
        
        if [ $? -eq 0 ]; then
            echo -e "  ${GREEN}✓ Created synchole-${BPM}bpm.syx${NC}"
        else
            echo -e "  ${YELLOW}⚠ SysEx conversion failed${NC}"
        fi
    else
        echo -e "  ${YELLOW}⚠ Compile failed${NC}"
    fi
done

# Restore original
echo -e "\n${BLUE}Restoring original source...${NC}"
cp "$PROJECT_DIR/${SOURCE_FILE}.original" "$PROJECT_DIR/$SOURCE_FILE"

echo -e "\n${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}   Build complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo
echo "Firmware files created in:"
echo "  $OUTPUT_DIR"
echo
ls -lh "$OUTPUT_DIR"/*.syx 2>/dev/null || echo "No .syx files created"
echo
