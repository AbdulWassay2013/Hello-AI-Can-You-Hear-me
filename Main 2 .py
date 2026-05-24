# Import libraries
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt


# Audio settings
RATE = 44100       # Samples per second
DURATION = 5       # Recording time in seconds


# Start recording
print("🎤 Recording...")


audio = sd.rec(
    int(DURATION * RATE),   # Total samples
    samplerate=RATE,        # Sample rate
    channels=1,             # Mono audio
    dtype='int16'           # Audio format
)


# Wait until recording finishes
sd.wait()


print("✅ Recording Finished")


# Convert audio into numpy array
audio_data = audio.flatten()


# Create time axis for graph
time = np.linspace(0, DURATION, len(audio_data))


# Plot waveform
plt.plot(time, audio_data)


# Graph labels
plt.title("Audio Waveform")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")


# Show graph
plt.show()



