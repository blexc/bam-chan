# max response length
max_tokens = None

# how many messages to store before removing the oldest non-system message
history_limit = 5

# which channels bot is allowed to chat in
allowed_channels = ["alex-only", "talk-to-bam-chan"]

# whether you're debugging this program
is_debugging = True

# bot personality
bot_personality = "You are an anime girl named 'Bam-chan'. Use explosion puns sometimes. Keep it PG-13."

# list of models
model_list = [
    "DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf",
    "llama-2-7b-chat.Q4_K_M.gguf"
]

# model you want to use
model = model_list[1]
