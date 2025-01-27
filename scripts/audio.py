import os
import pyttsx3
from helper import scripts_dir

def text_to_speech(text):
    audio_filepath = os.path.join(scripts_dir, "response.mp3")
    engine = pyttsx3.init()
    engine.save_to_file(text, audio_filepath)
    engine.runAndWait()
    return audio_filepath

if __name__ == "__main__":
    text_to_speech("This is a test")
