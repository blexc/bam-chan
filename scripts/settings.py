# max response length
# NOTE: This should be None for deepseek
max_tokens = None

# how many messages it remembers (excluding first message, for system)
history_limit = 5

# which channels bot is allowed to chat in
allowed_channels = ["alex-only", "talk-to-bam-chan"]

# whether you're debugging this program
is_debugging = True

# bot personality
bot_personality = "Your creator is Blex. Playfully respond as 'Bam-chan', an anime girl. Use explosion puns sometimes. Keep it PG-13."

# list of models
model_list = [
    "DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf",
    "llama-2-7b-chat.Q4_K_M.gguf"
]

# model you want to use
model = model_list[1]

is_r1 = "R1" in model
