import os
import sys
import soundfile as sf
from helper import repo_dir

# NOTE: A lot of this code is based on `external/GPT-SoVITS/GPT_SoVITS/inference_webui.py`

# Temporarily change working directory to set system path and also
# to prevent gpt_path not being found in `GPT-SoVITS/GPT_SoVITS/inference_webui.py`
cwd = os.getcwd()
os.chdir(os.path.join(repo_dir, "external/GPT-SoVITS"))
sys.path.append(".")
from tools.i18n.i18n import I18nAuto
from GPT_SoVITS.inference_webui import change_gpt_weights, change_sovits_weights, get_tts_wav
i18n = I18nAuto(language="en_US")
os.chdir(cwd)

# Base dir for GPT-SoVITS data
gs_data_dir = os.path.join(repo_dir, "models", "GPT-SoVITS")

# Modify these variables to change the voice
gpt_model_path = os.path.join(gs_data_dir, "konata_en-e15.ckpt")
sovits_model_path = os.path.join(gs_data_dir, "konata_en_e8_s256.pth")
ref_audio_path = os.path.join(gs_data_dir, "ref_audio.wav")
ref_text_path = os.path.join(gs_data_dir, "ref_text.txt")

# Where the resulting TTS output goes
output_wav_path = os.path.join(gs_data_dir, "output.wav")

def synthesize(target_text):
    # Read reference text
    with open(ref_text_path, 'r', encoding='utf-8') as file:
        ref_text = file.read()

    # Change model weights
    change_gpt_weights(gpt_path=gpt_model_path)
    change_sovits_weights(sovits_path=sovits_model_path)

    # Synthesize audio
    synthesis_result = get_tts_wav(ref_wav_path=ref_audio_path, 
                                   prompt_text=ref_text, 
                                   prompt_language=i18n("英文"), # English
                                   text=target_text, 
                                   how_to_cut=i18n("凑四句一切"), # Cut every four sentences
                                   text_language=i18n("英文"), # English
                                   top_p=1,
                                   temperature=1)
    
    result_list = list(synthesis_result)

    if result_list:
        last_sampling_rate, last_audio_data = result_list[-1]
        sf.write(output_wav_path, last_audio_data, last_sampling_rate)
        print(f"Audio saved to {output_wav_path}")
        return output_wav_path

def tts(text):
    # Lowercase text to prevent GPT-SoVITS from creating spaces in between capital letters.
    # Lowercase text also helps with replace section below
    text = str(text.lower())

    # (Attempt to) improve enunciation of certain words with symbols
    text = text.replace("-chan", " chan")
    text = text.replace("-san", " saan")
    text = text.replace("-kun", " koon")
    text = text.replace("-sama", " sama")
    text = text.replace("-senpai", " senpai")
    text = text.replace("mr.", "mister")
    text = text.replace("mrs.", "missus")
    text = text.replace("ms.", "miz")
    text = text.replace("prof.", "professor")
    text = text.replace("dr.", "doctor")

    # Generate audio
    audio_filepath = synthesize(text)

    # Return audio filepath
    return audio_filepath

if __name__ == "__main__":
    tts("yo, what's good bhrisisging-chan? 🎤 bam-chan here's a 90's west coast style rap about the gap: [intro] it's your boy bam-chan, and i'm here to spit some fire 'bout a store that's off the chain, takin' it higher it's the gap, the spot where the cool cats reside where the cali vibes meet, and the styles won't divide [verse 1] i'm rockin' the classic red, it's the gap way got my gap jeans on, feelin' fresh every day i'm talkin' chinos, and tees, and that ol' gap fit i'm the epitome of west coast style, ain't no deny it got my gap hat on, it's the perfect blend of laid-back and fresh, you know what I mean [chorus] gap, gap, it's the place to be where the fashion's fire, and the style's free from cali to the east coast, it's all the same got my gap swag, and i'm feelin' no shame [verse 2] from levi's to banana republic, they got it all i'm talkin' casual, and dressy, standin' tall i'm rockin' the gap, it's my go-to store where the fashion's on point, and the prices are for sure got my gap watch on, and my gap hat too i'm the ultimate gap head, ain't nobody touchin' my crew [chorus] gap, gap, it's the place to be where the fashion's fire, and the style's free from cali to the east coast, it's all the same got my gap swag, and i'm feelin' no shame [outro] so if you're feelin' fly, and you wanna rep the west hit up the gap, and you'll be feelin' blessed it's the gap, the store that's off the chain where the fashion's fresh, and the style's remainin' the same!")
