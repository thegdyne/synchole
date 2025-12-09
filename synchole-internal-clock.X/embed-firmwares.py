#!/usr/bin/env python3
"""
Embed all .syx files into a self-contained HTML file
"""

import os
import base64
import json
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
BPM_BUILDS_DIR = SCRIPT_DIR / "bpm-builds"
ORIGINAL_FIRMWARE = SCRIPT_DIR / "synchole-original-v3.0.syx"
OUTPUT_HTML = SCRIPT_DIR / "synchole-complete.html"

print("=" * 50)
print("  SYNCHOLE Firmware Embedder")
print("=" * 50)
print()

# Read original firmware (if exists)
original_firmware_b64 = None
if ORIGINAL_FIRMWARE.exists():
    with open(ORIGINAL_FIRMWARE, 'rb') as f:
        data = f.read()
        original_firmware_b64 = base64.b64encode(data).decode('ascii')
        print(f"✓ Original firmware found: v3.0 ({len(data)} bytes)")
        print()
else:
    print("⚠ Original firmware not found (synchole-original-v3.0.syx)")
    print("  Skipping restore option")
    print()

# Read all .syx files
firmwares = {}
syx_files = sorted(BPM_BUILDS_DIR.glob("*.syx"))

if not syx_files:
    print("❌ No .syx files found in bpm-builds/")
    print("   Run ./build-comprehensive-library.sh first!")
    exit(1)

print(f"Found {len(syx_files)} BPM firmware files:")
for syx_file in syx_files:
    # Extract BPM from filename
    bpm = syx_file.stem.replace("synchole-", "").replace("bpm", "")
    
    # Read and encode
    with open(syx_file, 'rb') as f:
        data = f.read()
        b64 = base64.b64encode(data).decode('ascii')
        firmwares[int(bpm)] = b64
        print(f"  ✓ {bpm} BPM ({len(data)} bytes)")

print()
print(f"Total BPM firmwares embedded: {len(firmwares)}")
print()

# Create HTML with embedded firmwares
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SYNCHOLE Firmware Library</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Roboto+Mono:wght@400;700&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --bg-dark: #0a0a0a;
            --bg-panel: #1a1a1a;
            --bg-control: #252525;
            --accent-orange: #ff6b00;
            --accent-amber: #ffb700;
            --text-primary: #e0e0e0;
            --text-secondary: #888;
            --border: #333;
            --glow: rgba(255, 107, 0, 0.4);
        }
        
        body {
            font-family: 'Roboto Mono', monospace;
            background: var(--bg-dark);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            background-image: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,107,0,0.03) 2px, rgba(255,107,0,0.03) 4px);
        }
        
        .container { max-width: 900px; width: 100%; }
        
        .panel {
            background: var(--bg-panel);
            border: 2px solid var(--border);
            border-radius: 12px;
            padding: 50px;
            box-shadow: 0 0 0 1px rgba(255,107,0,0.1), 0 30px 80px rgba(0,0,0,0.6);
            position: relative;
        }
        
        .panel::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent-orange), transparent);
        }
        
        .header { text-align: center; margin-bottom: 50px; }
        
        h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 3rem;
            font-weight: 900;
            color: var(--accent-orange);
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 4px;
            text-shadow: 0 0 30px var(--glow);
        }
        
        .subtitle {
            color: var(--text-secondary);
            font-size: 0.95rem;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        
        .control-section {
            background: var(--bg-control);
            border: 2px solid var(--border);
            border-radius: 8px;
            padding: 50px;
            margin-bottom: 30px;
        }
        
        .bpm-display {
            font-family: 'Orbitron', sans-serif;
            font-size: 7rem;
            font-weight: 900;
            color: var(--accent-orange);
            text-align: center;
            margin: 30px 0;
            text-shadow: 0 0 40px var(--glow);
            letter-spacing: 8px;
        }
        
        .bpm-label {
            text-align: center;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.9rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 40px;
        }
        
        .bpm-slider-container { position: relative; width: 100%; padding: 20px 0; }
        
        .bpm-slider {
            width: 100%;
            height: 10px;
            background: linear-gradient(90deg, var(--border) 0%, var(--accent-amber) 50%, var(--accent-orange) 100%);
            border-radius: 10px;
            outline: none;
            -webkit-appearance: none;
            cursor: pointer;
        }
        
        .bpm-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 40px; height: 40px;
            background: var(--accent-orange);
            border: 4px solid var(--bg-panel);
            border-radius: 50%;
            cursor: grab;
            box-shadow: 0 0 25px var(--glow);
            transition: all 0.2s;
        }
        
        .bpm-slider::-webkit-slider-thumb:hover {
            transform: scale(1.15);
            box-shadow: 0 0 35px var(--glow);
        }
        
        .bpm-slider::-moz-range-thumb {
            width: 40px; height: 40px;
            background: var(--accent-orange);
            border: 4px solid var(--bg-panel);
            border-radius: 50%;
            cursor: grab;
            box-shadow: 0 0 25px var(--glow);
            transition: all 0.2s;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin: 40px 0;
        }
        
        .stat-box {
            background: rgba(255,107,0,0.05);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 20px;
            text-align: center;
        }
        
        .stat-label {
            font-size: 0.7rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }
        
        .stat-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            color: var(--accent-amber);
            font-weight: 700;
        }
        
        .availability {
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            border-radius: 6px;
        }
        
        .availability.available {
            background: rgba(0,255,0,0.1);
            border: 1px solid rgba(0,255,0,0.3);
        }
        
        .availability.unavailable {
            background: rgba(255,0,0,0.1);
            border: 1px solid rgba(255,0,0,0.3);
        }
        
        .availability-icon { font-size: 1.5rem; margin-right: 10px; }
        
        .availability-text {
            font-family: 'Orbitron', sans-serif;
            font-size: 0.85rem;
            letter-spacing: 1px;
        }
        
        .download-btn {
            width: 100%;
            padding: 25px;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 3px;
            background: var(--accent-orange);
            color: var(--bg-dark);
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 0 30px var(--glow);
            position: relative;
        }
        
        .download-btn:hover:not(:disabled) {
            background: var(--accent-amber);
            transform: translateY(-3px);
            box-shadow: 0 0 50px var(--glow);
        }
        
        .download-btn:disabled {
            background: var(--border);
            color: var(--text-secondary);
            cursor: not-allowed;
            box-shadow: none;
        }
        
        .info-panel {
            background: rgba(255,183,0,0.05);
            border-left: 4px solid var(--accent-amber);
            padding: 20px;
            margin: 30px 0;
            border-radius: 4px;
        }
        
        .info-title {
            font-family: 'Orbitron', sans-serif;
            color: var(--accent-amber);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }
        
        .info-text {
            color: var(--text-secondary);
            font-size: 0.85rem;
            line-height: 1.6;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 25px;
            border-top: 1px solid var(--border);
            color: var(--text-secondary);
            font-size: 0.75rem;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        
        .downloading { animation: pulse 1s infinite; }
        
        .restore-section {
            background: rgba(255,0,0,0.05);
            border: 2px solid rgba(255,0,0,0.3);
            border-radius: 8px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .restore-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
        }
        
        .restore-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2rem;
            color: var(--accent-amber);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }
        
        .restore-text {
            color: var(--text-secondary);
            font-size: 0.85rem;
            line-height: 1.6;
            margin-bottom: 20px;
        }
        
        .restore-btn {
            padding: 20px 40px;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.1rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            background: rgba(255,183,0,0.2);
            color: var(--accent-amber);
            border: 2px solid var(--accent-amber);
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .restore-btn:hover {
            background: var(--accent-amber);
            color: var(--bg-dark);
            transform: translateY(-2px);
        }
        
        .restore-btn:disabled {
            background: var(--border);
            color: var(--text-secondary);
            border-color: var(--border);
            cursor: not-allowed;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            
            .panel {
                padding: 20px;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            .subtitle {
                font-size: 0.75rem;
            }
            
            .control-section {
                padding: 25px;
            }
            
            .bpm-display {
                font-size: 4rem;
            }
            
            .bpm-label {
                font-size: 0.75rem;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
                gap: 15px;
            }
            
            .stat-value {
                font-size: 1.5rem;
            }
            
            .download-btn, .restore-btn {
                padding: 20px;
                font-size: 1rem;
            }
            
            .info-text {
                font-size: 0.75rem;
            }
            
            .restore-section {
                padding: 20px;
            }
            
            .restore-title {
                font-size: 1rem;
            }
        }
        
        @media (max-width: 480px) {
            .panel {
                padding: 15px;
            }
            
            h1 {
                font-size: 1.5rem;
                letter-spacing: 2px;
            }
            
            .control-section {
                padding: 20px;
            }
            
            .bpm-display {
                font-size: 3rem;
                letter-spacing: 4px;
            }
            
            .bpm-slider::-webkit-slider-thumb {
                width: 30px;
                height: 30px;
            }
            
            .bpm-slider::-moz-range-thumb {
                width: 30px;
                height: 30px;
            }
            
            .download-btn, .restore-btn {
                padding: 15px;
                font-size: 0.9rem;
                letter-spacing: 1px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="panel">
            <div class="header">
                <h1>SYNCHOLE</h1>
                <div class="subtitle">Firmware Library v1.0</div>
            </div>
            
            ''' + ('''<div class="restore-section" id="restoreSection">
                <div class="restore-icon">⚠️</div>
                <div class="restore-title">Restore Original Firmware</div>
                <div class="restore-text">
                    This page contains modified firmware with internal clock mode.<br>
                    Click below to download the original SYNCHOLE firmware v3.0.
                </div>
                <button class="restore-btn" id="restoreBtn">
                    DOWNLOAD ORIGINAL v3.0
                </button>
            </div>
            ''' if original_firmware_b64 else '') + '''
            
            <div class="control-section">
                <div class="bpm-display" id="bpmDisplay">120</div>
                <div class="bpm-label">BEATS PER MINUTE</div>
                
                <div class="bpm-slider-container">
                    <input type="range" id="bpmSlider" class="bpm-slider" 
                           min="60" max="240" value="120" step="1" />
                </div>
                
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-label">Period</div>
                        <div class="stat-value" id="periodDisplay">21ms</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Clock Rate</div>
                        <div class="stat-value" id="rateDisplay">48 Hz</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Loaded</div>
                        <div class="stat-value" id="loadedCount">0</div>
                    </div>
                </div>
                
                <div id="availability" class="availability available">
                    <span class="availability-icon">✓</span>
                    <span class="availability-text">FIRMWARE AVAILABLE</span>
                </div>
                
                <button class="download-btn" id="downloadBtn">
                    DOWNLOAD FIRMWARE
                </button>
            </div>
            
            <div class="info-panel">
                <div class="info-title">⚡ How to Flash</div>
                <div class="info-text">
                    1. Click DOWNLOAD FIRMWARE (saves to ~/Downloads)<br>
                    2. Hold RUN button on SYNCHOLE<br>
                    3. Power on (ALL LEDs solid)<br>
                    4. Release RUN<br>
                    5. Send .syx file via MIDI (use SysEx Librarian)<br>
                    6. Power cycle and enjoy!
                </div>
            </div>
            
            <div class="footer">
                SYNCHOLE © Sixty-four pixels ltd. | Firmware Library by thegdyne 2025
            </div>
        </div>
    </div>
    
    <script>
        // EMBEDDED FIRMWARES (base64 encoded)
        const FIRMWARES = ''' + json.dumps(firmwares, indent=8) + ''';
        
        // ORIGINAL FIRMWARE (if available)
        const ORIGINAL_FIRMWARE = ''' + (f'"{original_firmware_b64}"' if original_firmware_b64 else 'null') + ''';
        
        // State
        let currentBPM = 120;
        
        // Elements
        const bpmSlider = document.getElementById('bpmSlider');
        const bpmDisplay = document.getElementById('bpmDisplay');
        const periodDisplay = document.getElementById('periodDisplay');
        const rateDisplay = document.getElementById('rateDisplay');
        const loadedCount = document.getElementById('loadedCount');
        const downloadBtn = document.getElementById('downloadBtn');
        const availability = document.getElementById('availability');
        const restoreBtn = document.getElementById('restoreBtn');
        
        // Calculate timings
        function calculateTimings(bpm) {
            const period = Math.round(60000 / (bpm * 24));
            const rate = Math.round((bpm * 24) / 60);
            return { period, rate };
        }
        
        // Get closest available BPM
        function getClosestAvailable(bpm) {
            const bpms = Object.keys(FIRMWARES).map(Number);
            return bpms.reduce((prev, curr) => {
                return Math.abs(curr - bpm) < Math.abs(prev - bpm) ? curr : prev;
            });
        }
        
        // Update display
        function updateDisplay() {
            const { period, rate } = calculateTimings(currentBPM);
            bpmDisplay.textContent = currentBPM;
            periodDisplay.textContent = `${period}ms`;
            rateDisplay.textContent = `${rate} Hz`;
            
            const available = FIRMWARES.hasOwnProperty(currentBPM);
            
            if (available) {
                availability.className = 'availability available';
                availability.innerHTML = `
                    <span class="availability-icon">✓</span>
                    <span class="availability-text">FIRMWARE AVAILABLE</span>
                `;
                downloadBtn.disabled = false;
            } else {
                const closest = getClosestAvailable(currentBPM);
                availability.className = 'availability unavailable';
                availability.innerHTML = `
                    <span class="availability-icon">⚠</span>
                    <span class="availability-text">NOT AVAILABLE — CLOSEST: ${closest} BPM</span>
                `;
                downloadBtn.disabled = true;
            }
        }
        
        // Slider handler
        bpmSlider.addEventListener('input', (e) => {
            currentBPM = parseInt(e.target.value);
            updateDisplay();
        });
        
        // Download handler
        downloadBtn.addEventListener('click', () => {
            const b64data = FIRMWARES[currentBPM];
            if (!b64data) return;
            
            downloadBtn.textContent = 'DOWNLOADING...';
            downloadBtn.classList.add('downloading');
            
            // Convert base64 to binary
            const binaryString = atob(b64data);
            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }
            
            // Create download
            const blob = new Blob([bytes], { type: 'application/octet-stream' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `synchole-${currentBPM}bpm.syx`;
            a.click();
            URL.revokeObjectURL(url);
            
            // Success feedback
            downloadBtn.textContent = '✓ DOWNLOADED!';
            setTimeout(() => {
                downloadBtn.textContent = 'DOWNLOAD FIRMWARE';
                downloadBtn.classList.remove('downloading');
            }, 2000);
        });
        
        // Restore button handler
        if (restoreBtn && ORIGINAL_FIRMWARE) {
            restoreBtn.addEventListener('click', () => {
                restoreBtn.textContent = 'DOWNLOADING...';
                restoreBtn.classList.add('downloading');
                
                // Convert base64 to binary
                const binaryString = atob(ORIGINAL_FIRMWARE);
                const bytes = new Uint8Array(binaryString.length);
                for (let i = 0; i < binaryString.length; i++) {
                    bytes[i] = binaryString.charCodeAt(i);
                }
                
                // Create download
                const blob = new Blob([bytes], { type: 'application/octet-stream' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'synchole-original-v3.0.syx';
                a.click();
                URL.revokeObjectURL(url);
                
                // Success feedback
                restoreBtn.textContent = '✓ DOWNLOADED!';
                setTimeout(() => {
                    restoreBtn.textContent = 'DOWNLOAD ORIGINAL v3.0';
                    restoreBtn.classList.remove('downloading');
                }, 2000);
            });
        }
        
        // Initialize
        loadedCount.textContent = Object.keys(FIRMWARES).length;
        updateDisplay();
    </script>
</body>
</html>'''

# Write HTML file
with open(OUTPUT_HTML, 'w') as f:
    f.write(html_content)

print(f"✓ Created: {OUTPUT_HTML}")
print(f"  File size: {OUTPUT_HTML.stat().st_size / 1024:.1f} KB")
print()
print("Done! Open synchole-complete.html in your browser!")
print()
