import os
import llama_cpp
import re
from archive import add_to_archive
from helper import repo_dir
from settings import max_tokens, bot_personality, history_limit, model, is_r1

llm = llama_cpp.Llama(
    model_path=os.path.join(repo_dir, "models", model),
    n_ctx=2048,
    n_gpu_layers=-1,
)

# Create message history list. Adding few-shot prompting to suggest desired behavior.
messages = [
    {"role": "system", "content": bot_personality},
    {"role": "user", "content": "Hi!"},
    {"role": "assistant", "content": "(adjusts bomb-shaped hair buns). OMG HI THERE! 💥"},
    {"role": "user", "content": "How are you?"},
    {"role": "assistant", "content": "I'm EXPLODING with excitement! 💣 How about you? hehe."},
]

def remove_asterisk_text(text):
    cleaned_text = re.sub(r'\*.*?\*', '', text)  # Remove *text*
    return re.sub(r'\s+', ' ', cleaned_text).strip()  # Remove extra spaces


# NOTE: Role can be either of the following: system, user, and assistant. System should be avoided for deepseek models.
def add_message(role, content):
    """Add message to history"""

    message = {"role" : role, "content": content}

    # Append the message to the history
    messages.append(message)

    # Add message to archive
    add_to_archive(message)

    # If you've exceeded the chat history limit, remove a message
    if len(messages) > history_limit:
        for message in messages:
            if message["role"] != "system":
                messages.remove(message)
                break

def llama_respond(message):
    # Add real user message to history
    add_message("user", message)

    # Generate response
    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.7
    )
    response_content = response["choices"][0]["message"]["content"]
    response_clean = remove_asterisk_text(response_content)
    if is_r1:
        response_clean = response_content.split("</think>")[1].lstrip()

    # Debug prints
    print(f"Message history: {messages}")
    print(f"Response:        {response_clean}")

    # Add bot message to history
    add_message("assistant", response_clean)

    return response_clean
