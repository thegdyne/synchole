# SYNCHOLE - MIDI to DIN Sync Hub

Modified version with internal clock feature.

## Original Project

SYNCHOLE by hotchk155/Jason (Sixty-four pixels ltd.)
- Original repository: https://github.com/hotchk155/din-synch-hub
- Product page: http://six4pix.com/synchole

**Original Features:**
- Converts MIDI clock to DIN Sync24 format
- 7 buffered SYNC24 outputs
- MIDI Thru with near-zero latency
- Optically isolated MIDI input
- Manual run/stop button

## Internal Clock Modification

**Modified by:** thegdyne/Gareth - December 2025  
**License:** CC BY-NC 4.0 (same as original)

### What's New

This fork adds an **internal clock mode**, allowing SYNCHOLE to work as a standalone clock source without requiring an external MIDI master.

**New Features:**
- **Two operating modes:**
  - External MIDI (default): Original behavior
  - Internal Clock: Generates 120 BPM clock
- **Long press RUN button** (2 seconds): Toggle between modes
- **Short press RUN button**: Start/stop (unchanged)
- **LED feedback**: Different patterns indicate current mode

### How It Works

**External MIDI Mode (Default):**
- Device powers on in this mode
- Converts incoming MIDI clock to SYNC24
- LED behavior same as original firmware

**Internal Clock Mode:**
- Long press RUN button to activate
- Blue ACT LED pulses slowly when stopped
- Generates 120 BPM clock at 24 PPQN
- Perfect for standalone use with vintage gear

**Mode Switching:**
- Long press RUN (2+ seconds)
- Both LEDs flash briefly
- Mode persists until changed (resets to external on power cycle)

### Quick Start

**Using External MIDI Mode:**
1. Power on device (starts in external MIDI mode)
2. Connect MIDI clock source
3. Press RUN to start/stop

**Using Internal Clock Mode:**
1. Long press RUN button (2 seconds)
2. Both LEDs flash - now in internal mode
3. Blue LED pulses slowly
4. Press RUN to start internal 120 BPM clock
5. Long press again to return to external MIDI mode

### Technical Details

**Hardware:** PIC12F1822 microcontroller  
**Compiler:** Microchip XC8 v2.46+ (free version)  
**Clock Rate:** 120 BPM fixed (24 PPQN = 48 pulses/second)  
**Timing:** ~21ms period between pulses  
**Memory:** ~27% program space, ~20% RAM

### Building from Source

**Requirements:**
- MPLAB X IDE (Mac/Windows/Linux)
- XC8 Compiler (free version)
- Python 3 (for hex to syx conversion)
- SysEx Librarian (Mac) or MIDI-OX (Windows)

**Build Steps:**
```bash
# 1. Open project in MPLAB X
# Open: synchole-internal-clock.X

# 2. Build project (Cmd+B or F11)
# Produces: dist/default/production/*.hex

# 3. Convert to SysEx
cd synchole-internal-clock.X
./hextosyx.py b dist/default/production/*.hex synchole-internal.syx

# 4. Flash via MIDI bootloader
# - Hold RUN, power on, release (LEDs solid = bootloader)
# - Send .syx via SysEx Librarian
# - Wait for rapid blinking
# - Power cycle
```

**Quick Build:**
```bash
cd synchole-internal-clock.X
./build-and-flash.sh
```

### Repository Structure

```
synchole/
├── firmware/                    # Original firmware
│   ├── din-sync-hub.c          # SourceBoost version
│   └── Release/*.hex           # Compiled originals
├── hardware/                    # PCB design files
│   ├── din-synch-hub.sch
│   └── din-synch-hub.brd
├── docs/                        # Documentation
├── synchole-internal-clock.X/  # Modified firmware
│   ├── din-sync-hub-xc8-fixed_2.c  # XC8 source with internal clock
│   ├── hextosyx.py             # HEX to SysEx converter
│   ├── build-and-flash.sh      # Build automation
│   └── nbproject/              # MPLAB X project files
└── README.md                    # This file
```

### Files

**Source Code:**
- `synchole-internal-clock.X/din-sync-hub-xc8-fixed_2.c` - Main firmware source

**Tools:**
- `synchole-internal-clock.X/hextosyx.py` - Python tool to convert .hex to .syx
- `synchole-internal-clock.X/build-and-flash.sh` - Automated build script

**Original Files:**
- `firmware/` - Original SourceBoost C source and compiled hex files
- `hardware/` - Eagle PCB design files

### Changes from Original

1. **Ported to XC8 compiler** (from SourceBoost C)
2. **Added internal clock generator** using Timer0 interrupt
3. **Long press detection** on RUN button
4. **Mode switching** with visual feedback
5. **Enhanced LED patterns** for mode indication

**Code Changes:**
- ~180 lines added/modified
- New variables: `bClockMode`, `bInternalClockCounter`, `bModeLEDCounter`
- New function: `generate_internal_clock_pulse()`
- Enhanced switch handler with long press detection
- Mode-aware MIDI processing

### Known Limitations

- **Fixed BPM:** Internal clock is hardcoded to 120 BPM
- **No mode persistence:** Reverts to external MIDI on power cycle
- **No MIDI in internal mode:** MIDI messages ignored when in internal mode

### Future Enhancement Ideas

- Variable BPM (tap tempo or preset selection)
- Save mode to EEPROM (remember on power up)
- MIDI thru/merge in internal mode
- Multiple BPM presets
- External CV clock input

### Troubleshooting

**LEDs stay on permanently:**
- Reflash firmware - may be incomplete upload

**Clock runs very slowly:**
- Check you're in correct mode
- Long press to switch modes

**Can't enter bootloader:**
- Hold RUN button BEFORE powering on
- Keep holding until both LEDs solid
- Then release and send firmware

**MIDI not working:**
- Ensure you're in external MIDI mode (not internal)
- Long press to switch if needed

### License

This modification maintains the original Creative Commons license:

**CC BY-NC 4.0** (Attribution-NonCommercial 4.0 International)

- ✅ Share and adapt freely
- ✅ Attribute original and modified work
- ❌ No commercial use

### Credits

**Original Design:** hotchk155 (Jason) - Sixty-four pixels ltd.  
**Internal Clock Mod:** thegdyne (Gareth) - December 2025  
**License:** CC BY-NC 4.0

### Contact

**For this modification:**
- GitHub: @thegdyne
- Fork: https://github.com/thegdyne/synchole

**For original SYNCHOLE:**
- Website: http://six4pix.com/synchole
- Email: sixtyfourpixels@gmail.com
- GitHub: https://github.com/hotchk155/din-synch-hub

### Changelog

**v4 - December 9, 2025**
- Added internal clock mode with 120 BPM generation
- Long press RUN button toggles modes
- LED pattern indicates current mode
- Ported from SourceBoost C to XC8 compiler
- Fixed Timer0 interrupt flag names for XC8
- Fixed switch polarity (active LOW)
- Fully tested on hardware

**v3 - August 14, 2016** (Original)
- Initial release with switch
- MIDI to SYNC24 conversion
- 7 buffered outputs

**v2 - December 12, 2015** (Original)
- New PCB revision

**v1 - November 19, 2015** (Original)
- Initial version
