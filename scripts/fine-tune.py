from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth import is_bfloat16_supported
import torch

import os
from helper import repo_dir

# This script when run as main will fine-tune a dataset

models_to_try = [
    "unsloth/Meta-Llama-3.1-8B-bnb-4bit",
    "unsloth/Meta-Llama-3.1-8B",
]

model_name = os.path.join(repo_dir, "models", "Meta-Llama-3.1-8B")
max_seq_length = 2048
dtype = None
load_in_4bit = True
bamchan_prompt = """Below is an input message that is part of a longer conversation. Write a response that appropriately completes the request.

### Input:
{}

### Response:
{}"""




if __name__ == "__main__":

    # Load model
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = model_name,
        max_seq_length = max_seq_length,
        dtype = dtype,
        load_in_4bit = load_in_4bit,
    )

    # Add LoRA adapters to save memory usage
    model = FastLanguageModel.get_peft_model(
        model,
        r = 16,
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj",],
        lora_alpha = 16,
        lora_dropout = 0,
        bias = "none",
        use_gradient_checkpointing = "unsloth",
        random_state = 3407,
        use_rslora = False,
        loftq_config = None,
    )

    EOS_TOKEN = tokenizer.eos_token # Must add EOS_TOKEN
    def formatting_prompts_func(examples):
        inputs       = examples["input"]
        outputs      = examples["output"]
        texts = []
        for input, output in zip(inputs, outputs):
            # Must add EOS_TOKEN, otherwise your generation will go on forever!
            text = bamchan_prompt.format(input, output) + EOS_TOKEN
            texts.append(text)
        return { "text" : texts, }

    dataset = load_dataset("blexchapman/bam-chan", split = "train")
    dataset = dataset.map(formatting_prompts_func, batched = True,)

    # Train model
    trainer = SFTTrainer(
        model = model,
        tokenizer = tokenizer,
        train_dataset = dataset,
        dataset_text_field = "text",
        max_seq_length = max_seq_length,
        dataset_num_proc = 2,
        packing = False, # Can make training 5x faster for short sequences.
        args = TrainingArguments(
            per_device_train_batch_size = 2,
            gradient_accumulation_steps = 4,
            warmup_steps = 5,
            # num_train_epochs = 1, # Uncomment this for 1 full training run.
            max_steps = 60, # 60 for fast run, None for full training run.
            learning_rate = 2e-4,
            fp16 = not is_bfloat16_supported(),
            bf16 = is_bfloat16_supported(),
            logging_steps = 1,
            optim = "adamw_8bit",
            weight_decay = 0.01,
            lr_scheduler_type = "linear",
            seed = 3407,
            output_dir = "outputs",
            report_to = "none", # Use this for WandB etc
        ),
    )

    trainer_stats = trainer.train()

    # Test model
    FastLanguageModel.for_inference(model) # Enable native 2x faster inference
    messages = [
        {"role": "system", "content": "You are an anime girl named 'Bam-chan'. Use explosion puns sometimes. Keep it PG-13."},
        {"role": "user", "content": "What does your hair look like?"},
    ]
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize = True,
        add_generation_prompt = True, # Must add for generation
        return_tensors = "pt",
    ).to("cuda")
    outputs = model.generate(input_ids = inputs, max_new_tokens = 240, use_cache = True,
                            temperature = 1.5, min_p = 0.1)
    print(tokenizer.decode(outputs[0]))

    # Convert to GGUF and upload model to huggingface 
    model_name = model_name.split("/")[1]
    model.save_pretrained_gguf(f"blexchapman/{model_name}-bam-chan", tokenizer, quantization_method = "q4_k_m")
