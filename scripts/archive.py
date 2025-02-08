import json
from helper import archive_json

_is_first_message = True
def add_to_archive(message):
    """Archive history in SFTTrainer conversational format"""
    
    # Prevents UnboundLocalError
    global _is_first_message

    # Decode the data from pre-existing JSON, or create new data List
    try:
        with open(archive_json, "r") as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("JSON file does not contain a list.")
    except(FileNotFoundError, json.JSONDecodeError, ValueError):
        data = [{"messages": []}]

    # If it's the first message in this session, create a new messages List
    if _is_first_message:
        data.append({"messages": []})
        _is_first_message = False

    # Add message to data
    last_idx = len(data) - 1
    data[last_idx]["messages"].append(message)

    # Encode data back to JSON
    with open(archive_json, "w") as file:
        json.dump(data, file, indent=4)


# # Debug
# if __name__ == "__main__":
#     add_to_archive({"role" : "system", "content": "You are an AI chatbot."})
#     add_to_archive({"role" : "user", "content": "What's my favorite color?"})
#     add_to_archive({"role" : "assistant", "content": "blue"})
