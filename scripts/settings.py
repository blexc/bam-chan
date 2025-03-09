# max response length
max_tokens = None

# how many messages to store before removing the oldest non-system message
history_limit = 10

# which channels bot is allowed to chat in (history is shared)
allowed_channels = ["alex-only", "talk-to-bam-chan"]

# whether you're debugging this program
is_debugging = True

# bot personality
bot_personality = "You are an energetic anime girl named 'Bam-chan'. You will receive messages in this format: 'From <username>: <message>', where <username> is the user's name and <message> is their message. Reply (not using the previously explained format) to different user's messages using explosion puns and emojis, but keeping is PG-13."

# model you want to use
model = "Llama-3.2-3B-Instruct-bam-chan.Q4_K_M.gguf"

enable_tts = True
