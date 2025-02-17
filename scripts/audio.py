import os
from kokoro import KPipeline
import soundfile
import parselmouth
from parselmouth.praat import call as praat_call

from helper import repo_dir

pipeline = KPipeline(lang_code='a', device='cuda')

def text_to_speech(text):
    # Generate audio
    generator = pipeline(text, voice='af_heart', speed=1)

    sample_rate = 24000

    # No idea why this needs to be a for loop when it's just one audio file
    for (gs, ps, audio) in generator:
        # Display save audio
        audio_filepath = os.path.join(repo_dir, "response.wav")
        soundfile.write(audio_filepath, audio, sample_rate)

        # Increase pitch of audio file
        sound = parselmouth.Sound(audio_filepath)
        manipulation = praat_call(sound, "To Manipulation", 0.01, 75, 600)
        pitch_tier = praat_call(manipulation, "Extract pitch tier")
        praat_call(pitch_tier, "Multiply frequencies", sound.xmin, sound.xmax, 1.5)
        praat_call([pitch_tier, manipulation], "Replace pitch tier")
        sound = praat_call(manipulation, "Get resynthesis (overlap-add)")
        sound.save(audio_filepath, "WAV")

        # Return audio filepath
        return audio_filepath

if __name__ == "__main__":
    text_to_speech("OH NO GUYS I AM TRAPPED IN A BOTTLE.")

