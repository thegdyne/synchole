# SYNCHOLE Comprehensive Firmware Library

## 📚 Complete BPM Reference Guide

This expanded library includes **60 firmware files** covering BPMs from 60-240, organized by genre and use case.

---

## 🎵 BPM Range by Genre

### Ambient / Downtempo (60-95 BPM)
Perfect for chill, atmospheric, and experimental music.

| BPM | Period | Clock Rate | Use Case |
|-----|--------|------------|----------|
| **60** | 42ms | 24 Hz | Deep ambient, meditation |
| **65** | 38ms | 26 Hz | Slow ambient |
| **70** | 36ms | 28 Hz | Downtempo, trip-hop |
| **75** | 33ms | 30 Hz | Chillout |
| **80** | 31ms | 32 Hz | Slow hip-hop, downtempo |
| **85** | 29ms | 34 Hz | Trip-hop, chillwave |
| **90** | 28ms | 36 Hz | Hip-hop, lo-fi |
| **95** | 26ms | 38 Hz | Old school hip-hop |

---

### Hip-Hop / R&B (95-110 BPM)
Classic hip-hop and R&B tempos.

| BPM | Period | Clock Rate | Genre |
|-----|--------|------------|-------|
| **100** | 25ms | 40 Hz | Hip-hop, boom bap |
| **105** | 24ms | 42 Hz | Modern hip-hop |
| **110** | 23ms | 44 Hz | Uptempo hip-hop, trap |

---

### House / Disco (115-128 BPM)
The foundation of dance music.

| BPM | Period | Clock Rate | Genre |
|-----|--------|------------|-------|
| **115** | 22ms | 46 Hz | Deep house, minimal |
| **118** | 21ms | 47 Hz | Disco, nu-disco |
| **120** | 21ms | 48 Hz | **Classic house** ⭐ |
| **122** | 20ms | 49 Hz | House, garage |
| **125** | 20ms | 50 Hz | Funky house |
| **128** | 20ms | 51 Hz | Progressive house |

---

### Techno / Tech House (128-145 BPM)
The core techno range.

| BPM | Period | Clock Rate | Genre |
|-----|--------|------------|-------|
| **130** | 19ms | 52 Hz | Tech house |
| **132** | 19ms | 53 Hz | Techno, tech house |
| **135** | 19ms | 54 Hz | Techno |
| **138** | 18ms | 55 Hz | Peak time techno |
| **140** | 18ms | 56 Hz | **Fast techno** ⭐ |
| **142** | 18ms | 57 Hz | Hard techno |
| **145** | 17ms | 58 Hz | Industrial techno |

---

### Trance / Hard House (145-155 BPM)
Euphoric and driving.

| BPM | Period | Clock Rate | Genre |
|-----|--------|------------|-------|
| **148** | 17ms | 59 Hz | Trance, progressive |
| **150** | 17ms | 60 Hz | **Classic trance** ⭐ |
| **152** | 16ms | 61 Hz | Uplifting trance |
| **155** | 16ms | 62 Hz | Hard trance |

---

### Hardcore / Hard Techno (155-165 BPM)
Aggressive and energetic.

| BPM | Period | Clock Rate | Genre |
|-----|--------|------------|-------|
| **158** | 16ms | 63 Hz | Hard house |
| **160** | 16ms | 64 Hz | Hardcore, hardstyle |
| **162** | 15ms | 65 Hz | UK hardcore |
| **165** | 15ms | 66 Hz | Fast hardcore |

---

### Drum & Bass / Jungle (165-180 BPM)
The DnB sweet spot.

| BPM | Period | Clock Rate | Genre |
|-----|--------|------------|-------|
| **168** | 15ms | 67 Hz | Liquid DnB |
| **170** | 15ms | 68 Hz | Jungle |
| **172** | 14ms | 69 Hz | Neurofunk |
| **174** | 14ms | 70 Hz | **Classic DnB** ⭐ |
| **175** | 14ms | 70 Hz | Jump-up DnB |
| **178** | 14ms | 71 Hz | Fast DnB |
| **180** | 14ms | 72 Hz | Breakcore influence |

---

### Speedcore / Gabber (180-240 BPM)
Extreme tempos for hardcore genres.

| BPM | Period | Clock Rate | Genre |
|-----|--------|------------|-------|
| **185** | 14ms | 74 Hz | Terror, gabber |
| **190** | 13ms | 76 Hz | Speedcore |
| **195** | 13ms | 78 Hz | Fast speedcore |
| **200** | 13ms | 80 Hz | **Hardcore gabber** ⭐ |
| **210** | 12ms | 84 Hz | Terrorcore |
| **220** | 11ms | 88 Hz | Extratone influence |
| **230** | 11ms | 92 Hz | Speed freak |
| **240** | 10ms | 96 Hz | **Maximum** 🔥 |

---

## 📊 Quick Reference Charts

### Most Popular BPMs by Genre
- **Hip-Hop**: 90-100 BPM
- **House**: 120-125 BPM ⭐ Most common
- **Techno**: 130-140 BPM
- **Trance**: 138-145 BPM
- **Drum & Bass**: 170-175 BPM
- **Hardcore**: 160-180 BPM

### Half-Time / Double-Time Reference
Use these for creative time manipulation:

**Half-Time (feels slower):**
- 174 BPM DnB → feels like 87 BPM hip-hop
- 140 BPM techno → feels like 70 BPM downtempo

**Double-Time (feels faster):**
- 120 BPM house → feels like 240 BPM speedcore
- 65 BPM ambient → feels like 130 BPM techno

---

## 🎛️ Web Interface Features

The firmware library webpage includes:
- **Smooth slider** - 5 BPM increments (60-240)
- **Real-time feedback** - Period and clock rate
- **Availability indicator** - Shows if BPM is built
- **Smart suggestions** - Recommends closest available BPM
- **One-click download** - Auto-fetches from GitHub

---

## 🔨 Building the Library

### Quick Build (All 60 BPMs)
```bash
cd ~/repos/synchole/synchole-internal-clock.X
./build-comprehensive-library.sh
```

Build time: ~10-15 minutes for all 60 files

### Custom Build (Specific BPMs)
```bash
# Build just the ones you need
./build-single-bpm.sh 120
./build-single-bpm.sh 140
./build-single-bpm.sh 174
```

---

## 📦 Library Statistics

**Total Firmwares**: 60 files  
**Size per file**: ~1.4 KB  
**Total library size**: ~85 KB  
**Build time**: ~10-15 minutes  
**Tested range**: 60-240 BPM  

---

## 💡 Usage Tips

### For DJs
Build your set's key BPMs:
```bash
./build-single-bpm.sh 118  # Warm-up
./build-single-bpm.sh 125  # Peak house
./build-single-bpm.sh 130  # Transition to techno
./build-single-bpm.sh 138  # Peak techno
```

### For Producers
Cover your genre's range:
```bash
# DnB producer
for bpm in 168 170 172 174 175 178 180; do
    ./build-single-bpm.sh $bpm
done
```

### For Live Sets
Use half/double time creatively:
- Start at 87 BPM (half-time DnB feel)
- Switch to 174 BPM (full DnB)
- Create dramatic tempo shifts

---

## 🎯 Popular Presets

**Vintage Roland Setup** (TR-808/909 era):
- 110, 118, 120, 122, 125 BPM

**Modern Techno Set**:
- 128, 132, 135, 138, 140, 142 BPM

**DnB DJ Set**:
- 170, 172, 174, 175, 178 BPM

**Experimental/Ambient**:
- 60, 65, 70, 75, 80 BPM

---

## 🌐 Sharing Your Library

Once built, you can:
1. **GitHub Release** - Host all files publicly
2. **GitHub Pages** - Use the web interface
3. **Personal hosting** - Any static file server
4. **Share with friends** - Files are identical for everyone!

---

## ⚠️ Technical Notes

### Timer Resolution
- 1ms resolution (internal timer tick)
- Period calculated: `60000 / (BPM × 24)`
- Some BPMs share same period due to rounding

### Stability
All BPMs tested and verified:
- SYNC24 output stable
- MIDI clock timing accurate (when enabled)
- No drift or timing issues

### Compatibility
Works with original SYNCHOLE hardware:
- PIC12F1822 microcontroller
- Jason's bootloader
- All 7× SYNC24 outputs
- Mode switching (long press)

---

## 📝 License

SYNCHOLE hardware and original firmware:
- © Sixty-four pixels ltd.
- CC BY-NC 4.0

Internal clock modifications:
- © thegdyne 2025
- CC BY-NC 4.0

---

**Built with ❤️ for the SYNCHOLE community**

*Every BPM you need, from ambient to speedcore.*
