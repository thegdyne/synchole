# SYNCHOLE Internal Clock - Quick Start

## What This Does

Adds internal 120 BPM clock to SYNCHOLE so it can work standalone without MIDI.

---

## Using the Device

### External MIDI Mode (Default)

**Power on** → Device starts in external MIDI mode

1. Connect MIDI clock source
2. Short press RUN to start/stop
3. Works exactly like original SYNCHOLE

### Internal Clock Mode

**Switch to internal mode:**
1. **Long press RUN** (hold 2+ seconds)
2. Both LEDs flash
3. Blue ACT LED pulses slowly

**Start the clock:**
1. **Short press RUN**
2. Clock generates at 120 BPM
3. Orange BEAT LED blinks every 24 pulses

**Switch back to external:**
1. **Long press RUN** (hold 2+ seconds)
2. Back to MIDI mode

---

## Building Firmware

### Requirements
- MPLAB X IDE
- XC8 Compiler (free)
- Python 3
- SysEx Librarian (Mac) or MIDI-OX (Windows)

### Build Steps

```bash
# 1. Open MPLAB X project
cd /path/to/synchole/synchole-internal-clock.X

# 2. Build in MPLAB X (Cmd+B)

# 3. Convert to SysEx
./hextosyx.py b dist/default/production/*.production.hex synchole-mod.syx

# 4. Flash firmware
# - Hold RUN, power on device
# - Release when LEDs solid (bootloader mode)
# - Send .syx file via SysEx Librarian
# - Wait for rapid LED blinking
# - Power cycle
```

### Or Use Helper Script

```bash
./build-and-flash.sh
# Follow on-screen instructions
```

---

## LED Indicators

### External MIDI Mode
- **PWR (red):** Always on
- **ACT (blue):** Blinks with MIDI activity
- **BEAT (orange):** Blinks with beat when running

### Internal Mode (Stopped)
- **PWR (red):** Always on
- **ACT (blue):** Pulses slowly (~500ms cycle)
- **BEAT (orange):** Off

### Internal Mode (Running)
- **PWR (red):** Always on
- **ACT (blue):** Off
- **BEAT (orange):** Blinks every 24 pulses

### Mode Change
- **Both ACT and BEAT:** Flash briefly

---

## Troubleshooting

**Q: LEDs all stay on**
- Reflash firmware - may be incomplete

**Q: Clock too slow**
- Wrong mode - long press to switch

**Q: Button not working**
- Hold for full 2 seconds for long press
- Try medium-length press (0.5 sec) for short press

**Q: Can't enter bootloader**
- Hold RUN BEFORE powering on
- Keep holding until LEDs solid
- Then release

---

## Technical Specs

- **Internal BPM:** 120 (fixed)
- **PPQN:** 24 (SYNC24 standard)
- **Pulse rate:** 48/second
- **Memory:** ~27% program, ~20% RAM
- **Compiler:** XC8 v2.46+

---

## Quick Reference Card

```
┌─────────────────────────────────────────┐
│  SYNCHOLE Internal Clock Mod            │
│  Version 4 - December 2025              │
├─────────────────────────────────────────┤
│  BUTTON ACTIONS:                        │
│  • Short press: Start/Stop              │
│  • Long press (2s): Toggle mode         │
├─────────────────────────────────────────┤
│  MODES:                                 │
│  • External MIDI (default)              │
│    - ACT blinks with MIDI               │
│  • Internal Clock (120 BPM)             │
│    - ACT pulses when stopped            │
├─────────────────────────────────────────┤
│  BOOTLOADER:                            │
│  • Hold RUN + Power On                  │
│  • LEDs solid = ready                   │
│  • Send .syx file                       │
│  • Power cycle when done                │
└─────────────────────────────────────────┘
```

---

## Files You Need

- **Source:** `din-sync-hub-xc8-fixed_2.c`
- **Tool:** `hextosyx.py`
- **Helper:** `build-and-flash.sh`

---

## More Info

See main README.md for:
- Detailed documentation
- Code changes
- Future enhancements
- Full troubleshooting guide

---

**Modified by thegdyne/Gareth - December 2025**  
**Original by hotchk155/Jason**  
**License: CC BY-NC 4.0**
