# Music Visualizer

A real-time audio waveform visualizer built with Python, Matplotlib, and SoundDevice. The visualization displays audio input as vertical bars.

## Pros & Cons
Pros:
- Real-time audio visualization from system input (supports virtual audio devices like BlackHole on macOS).
- Full-screen, borderless window with no toolbar.

Cons:
- No cross-platform support, MacOS only.
- No in-app customization.
- Manual visualizer customization by code.

## Requirements
- Python 3.10+
- Packages: numpy, matplotlib, sounddevice, pyqt5

BlackHole (Installation guide:____)

## Setup
1.	Install dependencies:
``pip install numpy matplotlib sounddevice pyqt5``
2.	Ensure your audio input device is set up. For macOS, you can use BlackHole.
3.	Modify the device_name variable in code.py if your input device name differs (Default name is BlackHole)

## Usage

Run the visualizer:
``python3 code.py``

## Customization
- Bar Count: bars_count (default: 100)
- Amplification: amplify (default: 20)
- Decay Rate: decay_rate (default: 0.8)
- Smooth Factor: smooth_factor (default: 0.2)
- Waveform Color: Change the color of bars via the color parameter with for rect in bars: rect.set_color(...)
- Background Color: Set with fig.patch.set_facecolor(...) and ax.set_facecolor(...).

## Troubleshooting
- Qt5Agg errors: Ensure PyQt5 is installed.
- No sound detected: Verify the device_name matches a valid input device (sounddevice.query_devices()).
- Permissions: On macOS, allow microphone access for Python.

## License

MIT License — free to use and modify.