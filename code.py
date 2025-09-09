import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import rfft
from matplotlib.animation import FuncAnimation

samplerate = 44100
blocksize = 2048
bars_count = 100
amplify = 20   # make this higher if still too short
bar_heights = np.zeros(bars_count)  # global
decay_rate = 0.8  # lower is faster
smooth_factor = 0.2  # higher is smoother

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
    global latest_data, bar_heights

    # FFT on current block
    fft_data = np.abs(np.fft.rfft(latest_data))

    # Choose evenly spaced bins
    indices = np.linspace(0, len(fft_data) - 1, bars_count//2, dtype=int)
    heights_half = fft_data[indices]

    # Normalize
    if np.max(heights_half) > 0:
        heights_half = heights_half / np.max(heights_half)

    # Amplify
    heights_half = heights_half * amplify

    # Mirror the right half to the left for symmetry
    heights = np.concatenate((heights_half[::-1], heights_half))

    # Smooth & Decay
    bar_heights[:] = bar_heights * 0.5 + heights * 0.5  # adjust 0.5+0.5 for reactivity

    # Update bars
    for rect, h in zip(bars, bar_heights):
        rect.set_height(h)
        rect.set_y(-h/2)

    ax.set_ylim(-amplify*1.1, amplify*1.1)

    return bars

# Start stream
stream = sd.InputStream(device=device_info, channels=1,
                        samplerate=samplerate, blocksize=blocksize,
                        callback=audio_callback)
stream.start()

ani = FuncAnimation(fig, update, interval=30, blit=True)
plt.show()