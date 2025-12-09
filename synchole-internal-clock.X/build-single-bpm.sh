#!/bin/bash
#
# SYNCHOLE Single-BPM Builder
# Interactive script to build one BPM at a time
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}   SYNCHOLE Single-BPM Builder${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo

# Get BPM from user
if [ -z "$1" ]; then
    echo -e "${YELLOW}Usage: $0 <BPM>${NC}"
    echo "Example: $0 140"
    echo
    echo "Common BPMs: 60, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200, 240"
    exit 1
fi

BPM=$1
SOURCE_FILE="din-sync-hub-xc8-fixed_2.c"

echo -e "${GREEN}Building for ${BPM} BPM...${NC}"
echo

# Calculate period
PERIOD=$(python3 -c "print(int(round(60000 / ($BPM * 24))))")
echo -e "📊 Calculated period: ${PERIOD}ms"
echo

# Backup original if not already done
if [ ! -f "${SOURCE_FILE}.original" ]; then
    echo -e "${YELLOW}Creating backup of original source...${NC}"
    cp "$SOURCE_FILE" "${SOURCE_FILE}.original"
fi

# Modify source
echo -e "${BLUE}Modifying source code...${NC}"
cp "${SOURCE_FILE}.original" "$SOURCE_FILE"

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/#define INTERNAL_CLOCK_PERIOD_MS.*/#define INTERNAL_CLOCK_PERIOD_MS $PERIOD  \/\/ ${BPM} BPM/" "$SOURCE_FILE"
else
    # Linux
    sed -i "s/#define INTERNAL_CLOCK_PERIOD_MS.*/#define INTERNAL_CLOCK_PERIOD_MS $PERIOD  \/\/ ${BPM} BPM/" "$SOURCE_FILE"
fi

# Verify change
echo -e "${BLUE}Verifying change...${NC}"
grep "INTERNAL_CLOCK_PERIOD_MS" "$SOURCE_FILE"
echo

# Clean
echo -e "${BLUE}Cleaning previous build...${NC}"
make -f nbproject/Makefile-default.mk clean

# Build
echo -e "${BLUE}Compiling...${NC}"
echo -e "${YELLOW}(This may take a moment)${NC}"
if make -f nbproject/Makefile-default.mk; then
    echo
    echo -e "${GREEN}✓ Compilation successful!${NC}"
    echo
    
    # Check for hex file
    HEX_FILE=$(ls -t dist/default/production/*.hex 2>/dev/null | head -1)
    if [ -z "$HEX_FILE" ]; then
        echo -e "${RED}✗ No hex file found!${NC}"
        exit 1
    fi
    
    echo -e "📦 Hex file: $HEX_FILE"
    
    # Create output directory
    mkdir -p bpm-builds
    
    # Convert to SysEx
    echo
    echo -e "${BLUE}Converting to SysEx...${NC}"
    if ./hextosyx.py b "$HEX_FILE" "bpm-builds/synchole-${BPM}bpm.syx"; then
        echo
        echo -e "${GREEN}✓ Successfully created: bpm-builds/synchole-${BPM}bpm.syx${NC}"
        ls -lh "bpm-builds/synchole-${BPM}bpm.syx"
    else
        echo -e "${RED}✗ SysEx conversion failed${NC}"
        exit 1
    fi
else
    echo
    echo -e "${RED}✗ Compilation failed${NC}"
    exit 1
fi

# Restore original
echo
echo -e "${BLUE}Restoring original source...${NC}"
cp "${SOURCE_FILE}.original" "$SOURCE_FILE"

echo
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}   Build complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo
echo "Flash bpm-builds/synchole-${BPM}bpm.syx to your SYNCHOLE!"
echo
