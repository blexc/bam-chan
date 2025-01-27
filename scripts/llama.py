import os
from llama_cpp import Llama

current_dir = os.path.dirname(os.path.abspath(__file__))

llm = Llama(
    model_path=os.path.join(current_dir, "../models/llama-2-7b-chat.Q4_K_M.gguf"),
    chat_format="llama-2"
)

def llama_respond(personality, message):
    prompt=(
        f"[INST] <<SYS>>\n"
        f"{personality}<</SYS>>\n"
        f"{message}[/INST]\n"
    )

    output = llm(
        prompt,
        max_tokens=256,
        temperature=0.3,
        stop=["[INST]"],
        echo=False, # Enable for debugging
    )

    return output["choices"][0]["text"]

if __name__ == "__main__":
    print(llama_respond("You are an anime girl named 'Bam-chan'. Use puns relating to explosions in your response sometimes.", "Do you like pizza? Respond with EXACTLY 3 words."))
