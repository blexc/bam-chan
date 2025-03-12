![image](https://github.com/user-attachments/assets/659b39a1-52cb-4891-93f3-9b6e2b50e5ee)

Bam-chan is a AI chat bot with a strange personality that I created for my personal discord. It uses llama-3.2 for text and GPT-SoVITS for audio.

# Installing dependencies

### CUDA 12.6 (wsl-ubuntu)

```
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-6
```

### PyTorch and llama-cpp-python with GPU support

```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=75" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir --force-reinstall --upgrade --verbose
```

## GPT-SoVITS (optional)

```
git submodules --init
pip install -r external/GPT-SoVITS/requirements.txt
```

At the moment data used to generate TTS is stored in `models/GPT-SoVITS`. The four things that need to be stored there is the gpt model, sovits model, reference audio, and reference text. At the moment, these are hard-coded in `audio.py`, but should later-on have some default option that's always available. You can disable TTS in the `settings.py`.

# Fine-tuning language model with Unsloth

Bam-chan uses `unsloth/Llama-3.2-3B-Instruct` as a base model. I fine-tuned the model to give the responses more... personality. See `datasets` to view the dataset I used to fine-tune the model.

Gist of Google Colab I used to fine-tune model: https://gist.github.com/blexc/14f7fe9fce36ad60092bcb8d348071c4
