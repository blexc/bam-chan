import os
import sys
from helper import repo_dir

# Temporarily change working directory to set system path and also
# to prevent gpt_path not being found in `GPT-SoVITS/GPT_SoVITS/inference_webui.py`
cwd = os.getcwd()
os.chdir(os.path.join(repo_dir, "external/GPT-SoVITS"))
sys.path.append(".")
from GPT_SoVITS.inference_cli import synthesize
os.chdir(cwd)

# Base dir for GPT-SoVITS data
gs_data_dir = os.path.join(repo_dir, "models", "GPT-SoVITS")

gpt_model = os.path.join(gs_data_dir, "konata_en-e15.ckpt")
sovits_model = os.path.join(gs_data_dir, "konata_en_e8_s256.pth")
ref_audio = os.path.join(gs_data_dir, "ref_audio.wav")
ref_text = os.path.join(gs_data_dir, "ref_text.txt")

def tts(text):
    # Lowercase text to prevent GPT-SoVITS from creating spaces in between capital letters
    text = text.lower()

    # Write text to tmp file for GPT-SoVITS to read from
    target_text = "tmp.txt"
    with open(target_text, 'w') as file:
        file.write(text)

    # Path audio will be generated
    audio_filepath = os.path.join(gs_data_dir, "output.wav")

    # Generate audio
    synthesize(gpt_model, sovits_model, ref_audio, ref_text, "英文", target_text, "英文", gs_data_dir)

    # Return audio filepath
    return audio_filepath

if __name__ == "__main__":
    tts("OH NO GUYS I AM TRAPPED IN A BOTTLE.")
