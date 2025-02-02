import os
import llama_cpp
from helper import repo_dir
from settings import max_tokens, bot_personality, history_limit, model

llm = llama_cpp.Llama(
    model_path=os.path.join(repo_dir, "models", model),
    n_ctx=2048,
    n_gpu_layers=-1,
)

# Create message history list. Adding few-shot prompting to suggest desired behavior.
messages = [
    {"role": "user", "content": "Hi!"},
    {"role": "assistant", "content": "*Adjusts bomb-shaped hair buns*. OMG HI THERE! 💥"},
    {"role": "user", "content": "How are you?"},
    {"role": "assistant", "content": "I'm EXPLODING with excitement! 💣 How about you? hehe."},
]

# NOTE: Role can be either of the following: system, user, and assistant. System should be avoided for deepseek models.
def add_message(role, content):
    """Add message to history"""

    # Append the message to the history
    messages.append({"role" : role, "content": content})

    # If you've exceeded the chat history limit, remove the 2nd oldest chat message
    if len(messages) > history_limit:
        messages.remove(messages[0])

def llama_respond(message):
    # Generate summary
    add_message("user", "Summarize the chat conversation accurately and simply. Focus on main topics.")
    summary = llm.create_chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.5
    )
    summary_content = summary["choices"][0]["message"]["content"]
    summary_no_thoughts = summary_content.split("</think>")[1].lstrip()

    # Remove summary prompt from history
    messages.pop()

    # Add real user message to history
    add_message("user", message)

    # Create summarized message
    summarized_messages = [
        {"role" : "user", "content": f"{bot_personality}"},
        {"role" : "user", "content": f"Summary of messages: {summary_no_thoughts}"},
        {"role" : "user", "content": f"Respond to this message: {message}"}
    ]

    # Generate actual response using the summary
    response = llm.create_chat_completion(
        messages=summarized_messages,
        max_tokens=max_tokens,
        temperature=0.7
    )
    response_content = response["choices"][0]["message"]["content"]
    response_no_thoughts = response_content.split("</think>")[1].lstrip()

    # Debug prints
    print(f"Message history: {messages}")
    print(f"Summary used:    {summary_no_thoughts}")
    print(f"Response:        {response_no_thoughts}")

    print(f"JSON copy-paste:")
    print( "    {")
    print(f"        \"instruction\": \"Engage in a conversation with the user.\",")
    print(f"        \"input\": \"{message}\",")
    print(f"        \"output\": \"{response_no_thoughts}\"")
    print( "    },")

    # Add bot message to history
    add_message("assistant", response_no_thoughts)

    return response_no_thoughts
