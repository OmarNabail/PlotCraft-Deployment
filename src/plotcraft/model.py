"""Load the trained PlotCraft model and run ZeroGPU inference."""

import spaces
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.plotcraft.config import (
    MAX_NEW_TOKENS,
    MODEL_ID,
    MODEL_SUBFOLDER,
    SYSTEM_PROMPT,
)


# ZeroGPU emulates CUDA during application startup. Loading onto CUDA here lets
# the platform prepare the model once instead of transferring it per request.
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_ID,
    subfolder=MODEL_SUBFOLDER,
)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    subfolder=MODEL_SUBFOLDER,
    dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
).to("cuda")
model.eval()


@spaces.GPU(duration=120)
def generate_with_model(prompt: str) -> str:
    """Generate PlotCraft code with the full GRPO Qwen model."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    formatted_prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to("cuda")

    with torch.inference_mode():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=True,
            temperature=0.7,
            top_p=0.8,
            top_k=20,
            repetition_penalty=1.05,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    new_tokens = output_ids[0, inputs["input_ids"].shape[1] :]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
