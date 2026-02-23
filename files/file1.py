import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

# Constants
duration = 5  # seconds
sample_rate = 44100  # Hz

print("Recording audio for {} seconds...".format(duration))

# Record audio
audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
sd.wait()  # Wait until recording is finished

print("Recording complete!")

# Flatten the array
audio = audio.flatten()

# Plotting the waveform
plt.figure(figsize=(12, 4))
time = np.linspace(0, duration, len(audio))
plt.plot(time, audio, color='royalblue')
plt.title("Captured Audio Waveform")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.tight_layout()
plt.show()

