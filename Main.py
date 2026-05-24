# Import required libraries
import sounddevice as sd  # For recording audio
import numpy as np  # For numerical operations
import matplotlib.pyplot as plt  # For plotting graphs
import speech_recognition as sr  # For speech-to-text

# Audio settings
RATE = 16000  # Sample rate (16000 samples per second)


# Function to record audio
def record(msg):

    # Ask user to start recording
    input(f"\n🎤 {msg} (Press Enter to START)")

    print("Recording... Press Enter to STOP")

    # List to store audio chunks
    recording = []

    # Variable to stop recording
    stop = False

    import threading

    # Function that waits for Enter key to stop recording
    def stop_rec():
        nonlocal stop
        input()
        stop = True

    # Start stop-listener thread
    threading.Thread(target=stop_rec).start()

    # Callback function receives microphone audio continuously
    def callback(indata, frames, time, status):

        # Save incoming audio data
        recording.append(indata.copy())

    # Open microphone stream
    with sd.InputStream(samplerate=RATE, channels=1, dtype="int16", callback=callback):

        # Keep recording until Enter pressed
        while not stop:
            pass

    # Combine all chunks into one array
    audio = np.concatenate(recording, axis=0)

    # Convert numpy array to bytes
    return audio.tobytes()


# Function to analyze audio
def analyze(data):

    # Convert bytes into numpy array
    s = np.frombuffer(data, dtype=np.int16)

    # Duration in seconds
    duration = len(s) / RATE

    # Average loudness
    avg = np.mean(abs(s))

    # Maximum loudness
    mx = np.max(abs(s))

    return duration, avg, mx, s


# Function to convert speech into text
def transcribe(data):

    # Create recognizer object
    r = sr.Recognizer()

    try:
        # Create AudioData object
        audio = sr.AudioData(data, RATE, 2)

        # Use Google speech recognition
        text = r.recognize_google(audio)

        return text

    except:
        return "Could not transcribe"


# Function to show recording details
def show(label, stats, text):

    d, avg, mx, _ = stats

    print(f"\n--- {label} ---")
    print(f"Duration: {d:.2f}s")
    print(f"Average Loudness: {avg:.0f}")
    print(f"Maximum Loudness: {mx:.0f}")
    print("Text:", text)


# Function to compare recordings
def compare(a, b):

    print("\n=== COMPARISON ===")

    print("Longer Recording:", "Recording 1" if a[0] > b[0] else "Recording 2")

    print("Louder Recording:", "Recording 1" if a[1] > b[1] else "Recording 2")


# Function to plot waveforms
def plot(a, b):

    # Time axis for recording 1
    t1 = np.linspace(0, len(a[3]) / RATE, len(a[3]))

    # Time axis for recording 2
    t2 = np.linspace(0, len(b[3]) / RATE, len(b[3]))

    # Plot recording 1
    plt.subplot(2, 1, 1)
    plt.plot(t1, a[3])
    plt.title("Recording 1")

    # Plot recording 2
    plt.subplot(2, 1, 2)
    plt.plot(t2, b[3])
    plt.title("Recording 2")

    # Adjust spacing
    plt.tight_layout()

    # Show graph
    plt.show()


# ================= MAIN PROGRAM =================


# First recording
r1 = record("Recording 1: Speak normally")


# Analyze first recording
s1 = analyze(r1)


# Convert first recording to text
t1 = transcribe(r1)


# Show first recording details
show("Recording 1", s1, t1)


# Second recording
r2 = record("Recording 2: Speak louder/faster")


# Analyze second recording
s2 = analyze(r2)


# Convert second recording to text
t2 = transcribe(r2)


# Show second recording details
show("Recording 2", s2, t2)


# Compare recordings
compare(s1, s2)


# Plot waveforms
plot(s1, s2)
