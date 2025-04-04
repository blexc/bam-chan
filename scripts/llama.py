import os
import llama_cpp
import re
from archive import add_to_archive
from helper import repo_dir, is_r1
from settings import max_tokens, bot_personality, history_limit, model, is_debugging

# Init local model
llm = llama_cpp.Llama(
    model_path=os.path.join(repo_dir, "models", model),
    n_ctx=2048,
    n_gpu_layers=-1,
)

# Create message history list
messages = []


def all_lowercase_but_cap_words(text):
    """Makes all text lowercase, unless a word is all uppercase"""
    words = text.split()
    result = []

    for word in words:
        # Check if the word is all caps
        if word.isupper() and len(word) > 1:
            result.append(word)
        else:
            result.append(word.lower())

    return ' '.join(result)


def remove_asterisk_text(text):
    """Remove asterisks (in case LLM is terribly excitable)"""
    cleaned_text = re.sub(r'\*.*?\*', '', text)  # Remove *text*
    return re.sub(r'\s+', ' ', cleaned_text).strip()  # Remove extra spaces


def add_message(role, content):
    """Add message to history with one of the following roles: system, user, and assistant"""

    # Avoid system prompts with R1 models
    if role == "system" and is_r1:
        role = "user"

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


def llama_respond(username, message):
    """Given a message, generate a response from the LLM and store conversation"""

    # If you haven't yet, add system information
    if len(messages) == 0:
        add_message("system", bot_personality)

    # Append username to message in proper format
    message = f"From {username}: {message}"

    # Add real user message to history
    add_message("user", message)

    # Generate response
    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.7
    )

    # Grab just the response and clean it up
    response_content = response["choices"][0]["message"]["content"]
    response_clean = remove_asterisk_text(response_content)
    if is_r1:
        response_clean = response_content.split("</think>")[1].lstrip()
    response_clean = all_lowercase_but_cap_words(response_clean)

    # Debug prints
    if is_debugging:
        print(f"Message history: {messages}")
        print(f"Response:        {response_clean}")

    # Add bot message to history
    add_message("assistant", response_clean)

    return response_clean

# # Debug
# if __name__ == "__main__":
#     while True:
#         llama_respond(input("Enter username = "), input("Enter message = "))
