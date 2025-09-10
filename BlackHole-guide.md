# BlackHole Installation Guide (macOS)

BlackHole is a free, open-source virtual audio driver that allows you to route audio between applications on macOS (e.g., sending system audio to a Python visualizer).

## Requirements

- macOS 10.15 (Catalina) or later
- Homebrew (optional, but recommended)

## Installation

### Option 1: Download Installer
1. [Download the latest installer](https://existential.audio/blackhole)
2. Close all running audio applications
3. Open and install package

### Option 2: Install via Homebrew
- 2ch: brew install blackhole-2ch
- 16ch: brew install blackhole-16ch
- 64ch: brew install blackhole-64ch

## Configuration
1. Open Audio MIDI Setup (Applications → Utilities → Audio MIDI Setup).
2. You should see BlackHole 2ch in the device list, that means you installed it correctly.
3. To route system audio to BlackHole:
    1. Click the + button at the bottom-left → Create Multi-Output Device.
    2. Check BlackHole 2ch and your speakers/headphones.
    3. Set this device as your System Output in System Settings → Sound → Output.
    4. Test audio routing by playing a song and checking that your visualizer can capture it.

## Resources
- [BlackHole's Official Page](https://existential.audio/blackhole/)
- [BlackHole's GitHub Repository](https://github.com/ExistentialAudio/BlackHole)