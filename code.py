import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import rfft
from matplotlib.animation import FuncAnimation

samplerate = 44100
blocksize = 2048
bars_count = 100
amplify = 10   # make this higher if still too short

device_name = "BlackHole"

# Find BlackHole device index
device_info = None
for idx, dev in enumerate(sd.query_devices()):
    if device_name in dev['name']:
        device_info = idx
        break

if device_info is None:
    raise RuntimeError("BlackHole not found! Check Audio MIDI Setup.")

# Setup plot
fig, ax = plt.subplots()
bars = ax.bar(range(bars_count), np.zeros(bars_count), width=0.9)

ax.set_ylim(-1, 1)
ax.set_xlim(0, bars_count)
ax.set_title("Waveform Bars Visualizer")
ax.set_xlabel("Samples (chunked)")
ax.set_ylabel("Amplitude")

latest_data = np.zeros(blocksize)

# Audio callback
def audio_callback(indata, frames, time, status):
    global latest_data
    if status:
        print(status)
    latest_data = indata[:, 0]  # mono

def update(frame):
    global latest_data

    # Apply FFT on the current audio block
    fft_data = np.abs(rfft(latest_data))

    # Pick bars_count evenly spaced frequencies
    indices = np.linspace(0, len(fft_data) - 1, bars_count, dtype=int)
    heights = fft_data[indices]

    # Normalize so bars fit nicely
    if np.max(heights) > 0:
        heights = heights / np.max(heights)

    # Amplify peaks
    heights = heights * amplify

    # Update bars (centered, so they go both up & down)
    for rect, h in zip(bars, heights):
        rect.set_height(h)
        rect.set_y(-h / 2)

    ax.set_ylim(-amplify, amplify)

    return bars

# Start stream
stream = sd.InputStream(device=device_info, channels=1,
                        samplerate=samplerate, blocksize=blocksize,
                        callback=audio_callback)
stream.start()

ani = FuncAnimation(fig, update, interval=30, blit=True)
plt.show()