import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
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
fig.canvas.manager.set_window_title("Music Visualizer")

bars = ax.bar(range(bars_count), np.zeros(bars_count), width=0.9)

fig.patch.set_facecolor('black')
ax.set_facecolor('black')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

latest_data = np.zeros(blocksize)  # define globally
bar_heights = np.zeros(bars_count)  # keep this global too

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
    indices = np.linspace(0, len(fft_data) - 1, bars_count, dtype=int)
    heights = fft_data[indices]

    # Normalize
    if np.max(heights) > 0:
        heights = heights / np.max(heights)

    # Amplify peaks
    heights = heights * amplify

    # Smooth & decay for nicer look
    bar_heights[:] = bar_heights * decay_rate + heights * smooth_factor

    # Update bars (centered)
    for rect, h in zip(bars, bar_heights):
        rect.set_height(h)
        rect.set_y(-h/2)

    # Keep y-axis slightly bigger than amplify for padding
    ax.set_ylim(-amplify, amplify)

    return bars

# Start stream
stream = sd.InputStream(device=device_info, channels=1,
                        samplerate=samplerate, blocksize=blocksize,
                        callback=audio_callback)
stream.start()

ani = FuncAnimation(fig, update, interval=30, blit=True)
plt.show()