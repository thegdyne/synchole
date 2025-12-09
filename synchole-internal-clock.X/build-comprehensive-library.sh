#!/bin/bash
#
# SYNCHOLE Comprehensive Firmware Library Builder
# Builds firmware for extensive BPM range
#

set -e

# Configuration
SOURCE_FILE="din-sync-hub-xc8-fixed_2.c"
PROJECT_DIR="$HOME/repos/synchole/synchole-internal-clock.X"
OUTPUT_DIR="$PROJECT_DIR/bpm-builds"

# Comprehensive BPM library organized by genre/use case
BPMS=(
    # Ambient / Downtempo (60-95)
    60 65 70 75 80 85 90 95
    
    # Hip-Hop / Trip-Hop (95-110)
    100 105 110
    
    # House / Disco (115-128)
    115 118 120 122 125 128
    
    # Techno / Tech House (128-145)
    130 132 135 138 140 142 145
    
    # Trance / Hard House (145-155)
    148 150 152 155
    
    # Hardcore / Hard Techno (155-165)
    158 160 162 165
    
    # Drum & Bass / Jungle (165-180)
    168 170 172 174 175 178 180
    
    # Speedcore / Gabber (180-240)
    185 190 195 200 210 220 230 240
)

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}   SYNCHOLE Comprehensive Library Builder${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo
echo "Building ${#BPMS[@]} firmware files..."
echo

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Backup original source
if [ ! -f "$PROJECT_DIR/${SOURCE_FILE}.original" ]; then
    echo -e "${YELLOW}Backing up original source...${NC}"
    cp "$PROJECT_DIR/$SOURCE_FILE" "$PROJECT_DIR/${SOURCE_FILE}.original"
fi

# Build counter
SUCCESS=0
FAILED=0

# Build for each BPM
for BPM in "${BPMS[@]}"; do
    echo -e "\n${GREEN}Building ${BPM} BPM...${NC}"
    
    # Calculate period
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
    
    # Build in MPLAB X
    cd "$PROJECT_DIR"
    echo "  Compiling..."
    make -f nbproject/Makefile-default.mk clean > /dev/null 2>&1
    
    if make -f nbproject/Makefile-default.mk > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓ Compile successful${NC}"
        
        # Convert to SysEx
        echo "  Converting to .syx..."
        HEX_FILE=$(ls -t dist/default/production/*.hex 2>/dev/null | head -1)
        
        if ./hextosyx.py b "$HEX_FILE" "$OUTPUT_DIR/synchole-${BPM}bpm.syx" > /dev/null 2>&1; then
            echo -e "  ${GREEN}✓ Created synchole-${BPM}bpm.syx${NC}"
            ((SUCCESS++))
        else
            echo -e "  ${YELLOW}⚠ SysEx conversion failed${NC}"
            ((FAILED++))
        fi
    else
        echo -e "  ${YELLOW}⚠ Compile failed${NC}"
        ((FAILED++))
    fi
done

# Restore original
echo -e "\n${BLUE}Restoring original source...${NC}"
cp "$PROJECT_DIR/${SOURCE_FILE}.original" "$PROJECT_DIR/$SOURCE_FILE"

echo -e "\n${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}   Build complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo
echo "Results:"
echo "  ✓ Success: ${SUCCESS}"
echo "  ✗ Failed: ${FAILED}"
echo "  Total: ${#BPMS[@]}"
echo
echo "Firmware files created in:"
echo "  $OUTPUT_DIR"
echo
ls -lh "$OUTPUT_DIR"/*.syx 2>/dev/null | wc -l | xargs echo "Total files:"
echo
