# TODO

- [ ] Fine-tune model
- [ ] Fine-tune model using conversational formatting
- [ ] Fine-tune a reasoning model
- [ ] Try vision models
- [ ] Improve audio
    - [ ] Try kokoro again
    - [ ] Generating a cute voice rather than generic tts
    - [ ] When that bot is typing sound effects, make the sound effects rather than saying them
    - [ ] Resolve case when two audio files are generated at the same time
- [ ] Differentiate between users (add username to message, and perhaps add this information to dataset as well)
- [ ] Train secondary model with one token to generate emoji to react to message
- [ ] Automatically append chat history in JSON format to a single file (so I can pick messages I want to fine-tune with)
- [ ] Store chat history using `datasets` and make it conversational formatting

# Done

- [x] Only respond to certain discord channels
- [x] Remember some conversation history

# How to...

## Install CUDA 12.6 on WSL

```
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-6
```

## Install pytorch, unsloth, and llama-cpp-python with GPU support

```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install "unsloth[cu126-torch260] @ git+https://github.com/unslothai/unsloth.git"
CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=75" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir --force-reinstall --upgrade --verbose
```

## Download GGUF models

```bash
huggingface-cli download <repo_id> <model>.gguf --local-dir models
```

Note that models with a full directory are for fine tuning, whereas `.gguf` files are for running the llm via llama.
