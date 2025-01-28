import os
import llama_cpp
import helper
from settings import max_tokens, is_debugging, bot_personality, history_limit

llm = llama_cpp.Llama(
    model_path=os.path.join(helper.scripts_dir, "../models/llama-2-7b-chat.Q4_K_M.gguf"),
    chat_format="llama-2",
    n_gpu_layers=-1,
)

# Create message history list
messages = [
    {
        "role": "system",
        "content": bot_personality,
    },
]

def add_message(role, content):
    """Add message to history"""
    messages.append({"role" : role, "content": content})

    # If you've exceeded the chat history limit, remove the oldest chat message
    if len(messages) > history_limit:
        for message in messages:
            if message["role"] != "system":
                messages.remove(message)
                break

def llama_respond(message):
    # Add user message to history
    add_message("user", message)

    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=max_tokens,
    )
    response_content = response["choices"][0]["message"]["content"]

    # Add bot message to history
    add_message("assistant", response_content)

    return response_content
