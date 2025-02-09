![Screenshot 2025-02-08 160916](https://github.com/user-attachments/assets/1c54125c-dd74-473a-95bc-2ca1f7989876)

Bam-chan is a AI chat bot with a strange personality that I created for my personal discord.

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
