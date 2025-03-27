from gtts import gTTS
import os

def generate_tts(text, filename="output.mp3"):
    tts = gTTS(text, lang="hi")  
    tts.save(filename)
    return filename
