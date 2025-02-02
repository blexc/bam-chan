import os
import llama_cpp
from helper import repo_dir
from settings import max_tokens, bot_personality, history_limit, model

llm = llama_cpp.Llama(
    model_path=os.path.join(repo_dir, "models", model),
    n_ctx=2048,
    n_gpu_layers=20,
)

# Create message history list. Adding few-shot prompting to suggest desired behavior
messages = [
    {"role": "user", "content": bot_personality},
    {"role": "user", "content": "Hi!"},
    {"role": "assistant", "content": "*Adjusts bomb-shaped hair buns*. OMG HI THERE! 💥"},
    {"role": "user", "content": "How are you?"},
    {"role": "assistant", "content": "I'm EXPLODING with excitement! 💣 How about you? hehe."},
]

# NOTE: Role can be either of the following: system, user, and assistant
def add_message(role, content):
    """Add message to history"""

    # Append the message to the history
    messages.append({"role" : role, "content": content})

    # If you've exceeded the chat history limit, remove the 2nd oldest chat message
    if len(messages) > history_limit:
        messages.remove(messages[1])

def llama_respond(message):
    # Add user message to history
    add_message("user", message)

    # Generate response
    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.5
    )
    response_content = response["choices"][0]["message"]["content"]
    response_finish_reason = response['choices'][0]['finish_reason']

    # Split content between thoughts and its actual response
    response_content = response_content.split("</think>")

    # Error checking
    if len(response_content) < 2 or response_finish_reason != "stop":
        print(f"WARNING: response_finish_reason: {response_finish_reason}")
        print(f"WARNING: The llm failed to finish it's thoughts: {response_content}")
        return "That was too confusing for me."

    # Clear out thoughts for the response
    response_clean = response_content[1]

    # Add bot message to history
    add_message("assistant", response_clean)

    return response_clean
