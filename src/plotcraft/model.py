"""Load the trained PlotCraft model and run inference."""

from functools import lru_cache
from typing import Any

from src.plotcraft.config import (
    MAX_NEW_TOKENS,
    MODEL_ID,
    MODEL_SUBFOLDER,
    SYSTEM_PROMPT,
)


@lru_cache(maxsize=1)
def load_model() -> tuple[Any, Any]:
    """Download and load the tokenizer and full GRPO model once."""
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as error:
        raise RuntimeError(
            "Real model mode requires torch, transformers, and accelerate."
        ) from error

    if not torch.cuda.is_available():
        raise RuntimeError(
            "Real model mode requires a CUDA GPU. Use MODEL_MODE=mock locally."
        )

    compute_dtype = (
        torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    )

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        subfolder=MODEL_SUBFOLDER,
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        subfolder=MODEL_SUBFOLDER,
        dtype=compute_dtype,
        device_map="auto",
        low_cpu_mem_usage=True,
    )
    model.eval()
    return tokenizer, model


def generate_with_model(prompt: str) -> str:
    """Generate PlotCraft code with the full GRPO Qwen model."""
    import torch

    tokenizer, model = load_model()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    formatted_prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(model.device)

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
