import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
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

    # Split waveform into chunks
    chunked = np.array_split(latest_data, bars_count)
    heights = np.array([np.mean(np.abs(chunk)) for chunk in chunked])

    # Normalize to max of current frame
    if np.max(heights) > 0:
        heights = heights / np.max(heights)

    # Amplify
    heights = heights * amplify

    # Update bars (centered)
    for rect, h in zip(bars, heights):
        rect.set_height(h)
        rect.set_y(-h/2)

    # Keep y-axis fitting the amplification
    ax.set_ylim(-amplify, amplify)

    return bars

# Start stream
stream = sd.InputStream(device=device_info, channels=1,
                        samplerate=samplerate, blocksize=blocksize,
                        callback=audio_callback)
stream.start()

ani = FuncAnimation(fig, update, interval=30, blit=True)
plt.show()