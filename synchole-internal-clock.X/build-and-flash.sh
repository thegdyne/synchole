#!/bin/bash
#
# SYNCHOLE Build and Flash Workflow
# Run this after building in MPLAB X
#

set -e  # Exit on error

echo "================================"
echo "SYNCHOLE v4 - Build & Flash"
echo "================================"
echo ""

# Configuration
PRODUCT_ID="b"  # b = synchole
HEX_FILE="firmware.production.hex"
SYX_FILE="synchole-v4-internal-clock.syx"

# Check if we're in the right directory
if [ ! -f "hextosyx.py" ]; then
    echo "Error: hextosyx.py not found!"
    echo "Run this script from the firmware directory"
    exit 1
fi

# Make sure hextosyx.py is executable
chmod +x hextosyx.py

# Step 1: Find the HEX file
echo "Step 1: Locating HEX file..."
if [ ! -f "dist/default/production/${HEX_FILE}" ]; then
    echo "Error: HEX file not found at dist/default/production/${HEX_FILE}"
    echo "Have you built the project in MPLAB X?"
    exit 1
fi
echo "✓ Found: dist/default/production/${HEX_FILE}"
echo ""

# Step 2: Convert HEX to SysEx
echo "Step 2: Converting HEX to SysEx..."
./hextosyx.py ${PRODUCT_ID} "dist/default/production/${HEX_FILE}" "${SYX_FILE}"
if [ $? -ne 0 ]; then
    echo "Error: Conversion failed!"
    exit 1
fi
echo "✓ Created: ${SYX_FILE}"
echo ""

# Step 3: Instructions for flashing
echo "Step 3: Flash to device"
echo "================================"
echo ""
echo "Now follow these steps:"
echo ""
echo "1. HOLD the RUN button on SYNCHOLE"
echo "2. PLUG IN power (keep holding RUN)"
echo "3. Both LEDs should light SOLID"
echo "4. RELEASE the RUN button"
echo "5. Open SysEx Librarian"
echo "6. Set delay to 100ms in preferences"
echo "7. Drag ${SYX_FILE} into the window"
echo "8. Click 'Play' to send"
echo "9. Wait for LEDs to blink rapidly"
echo "10. UNPLUG power"
echo "11. PLUG IN power again"
echo "12. Done!"
echo ""
echo "================================"
echo ""
echo "SysEx file ready: ${SYX_FILE}"
echo ""
echo "To test:"
echo "  - Short press: start/stop"
echo "  - Long press (2s): toggle mode"
echo ""

# Optional: Open SysEx Librarian automatically (Mac only)
if [[ "$OSTYPE" == "darwin"* ]]; then
    read -p "Open SysEx Librarian now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open -a "SysEx Librarian" "${SYX_FILE}"
    fi
fi

echo "Done! Ready to flash."
