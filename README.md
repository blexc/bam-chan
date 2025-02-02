# TODO

- [ ] Fine-tune model
- [ ] Use a bigger model
- [ ] Improve audio
    - [ ] Generating a cute voice rather than generic tts
    - [ ] When that bot is typing sound effects, make the sound effects rather than saying them
    - [ ] Resolve case when two audio files are generated at the same time
- [ ] Differentiate between users
- [ ] Train secondary model with one token to generate emoji to react to message

# Done

- [x] Only respond to certain discord channels
- [x] Remember some conversation history

# Info

## How to download models

```bash
huggingface-cli download <repo_id> <model>.gguf --local-dir models
```
