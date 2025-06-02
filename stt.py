from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json

q = queue.Queue()

# Callback untuk audio input
def callback(indata, frames, time, status):
    q.put(bytes(indata))

# Load model
model = Model("vosk-model-small-en-us-0.15")  # Ganti sesuai lokasi model
rec = KaldiRecognizer(model, 16000, '["a", "b", "c", "d", "e", "f", "g", "h", "one", "two", "three", "four", "five", "six", "seven", "eight", "knight", "bishop", "king", "queen", "pawn", "rook"]')

# Mulai stream mikrofon
def micOn():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                        channels=1, callback=callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    text = text.split()
                    print("Terdeteksi:", text)
                    return text
    
                
def getText():
    return micOn()
# while True:
#     micOn()