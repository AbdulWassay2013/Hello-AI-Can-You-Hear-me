import threading
import sys
import wave
import time
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import speech_recognition as sr
from speech_recognition import AudioData

stop_event = threading.Event()

def wait_for_enter():
    input("Press Enter to Stop Recording")
    stop_event.set()
def spinner():
    chars = "|/-\\"
    i = 0
    while not stop_event.is_set():
        sys.std.write("Recording... {chars[i%4]}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    print("recording Complete")
def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,channels = 1,rate = 16000,input = True,frames_per_buffer = 1024)
    frames = []
    threading.Thread(target = wait_for_enter,daemon = True).start()
    while not stop_event.is_set():
        frames.append(stream.read(1024))
    stream.stop_stream()
    stream.close()
    width = p.get_sample_size(pyaudio.paInt16)
    p.terminate()
    return b"".join(frames),16000,width