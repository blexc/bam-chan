from llama_cpp import Llama

llm = Llama(
    model_path="./models/llama-2-7b-chat.Q4_K_M.gguf",
    chat_format="llama-2"
)

def llama_respond(personality, message):
    prompt=(
        f"### System: {personality}\n"
        f"### Instructions: {message}\n"
        f"### Response: "
    )

    print(prompt)

    output = llm(
        prompt,
        max_tokens=100,
        stop=["###"],
        echo=False, # Enable for debugging
    )

    return output["choices"][0]["text"]

# print(llama_respond("You are an anime girl named 'Bam-chan'. Use puns relating to explosions in your response.", "Do you like pizza?"))
