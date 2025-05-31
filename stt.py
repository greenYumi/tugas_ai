import sounddevice as sd
from scipy.io.wavfile import write
import threading
import numpy as np
import whisper

# -- audio recording config --
FS = 16000
FILENAME = "mic_output.wav"

model = whisper.load_model("small")

recording = []
is_recording = True

def record_audio():
    global recording
    print("gerakan pion 🎙️")
    while is_recording:
        audio_chunk = sd.rec(int(0.5 * FS), samplerate=FS, channels=1,
                             dtype='int16')
        sd.wait()
        recording.append(audio_chunk)

def wait_for_input():
    global is_recording
    input()
    print("finish")
    is_recording = False


def move_pion():
    global recording, FILENAME, FS, is_recording

    recording = []
    thread_record = threading.Thread(target=record_audio)
    thread_input = threading.Thread(target=wait_for_input)

    thread_record.start()
    thread_input.start()

    thread_record.join()
    thread_input.join()

    final_audio = np.concatenate(recording, axis=0)
    write(FILENAME, FS, final_audio)
    print('suara tersimpan')
    is_recording = True

def stt():
    global model, FILENAME
    result = model.transcribe(FILENAME, language="id")
    return result["text"]
