"""Application-level validation and PlotCraft generation service."""

from src.plotcraft.config import MAX_PROMPT_CHARACTERS, MODEL_MODE

if MODEL_MODE == "real":
    # Importing at startup is required so ZeroGPU can prepare the model on CUDA.
    from src.plotcraft.model import generate_with_model
else:
    generate_with_model = None


PLACEHOLDER_CODE = """import matplotlib.pyplot as plt

categories = ["Model A", "Model B", "Model C"]
scores = [0.78, 0.85, 0.91]

plt.bar(categories, scores)
plt.xlabel("Model")
plt.ylabel("Score")
plt.title("Model Comparison")
plt.show()
"""


def _remove_markdown_fences(generated_text: str) -> str:
    """Remove a single Markdown code fence around generated code."""
    cleaned = generated_text.strip()
    if not cleaned.startswith("```"):
        return cleaned

    lines = cleaned.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def generate_plot_code(prompt: str) -> str:
    """Validate a request and return plotting code."""
    cleaned_prompt = prompt.strip()

    if not cleaned_prompt:
        raise ValueError("Please enter a plotting request.")
    if len(cleaned_prompt) > MAX_PROMPT_CHARACTERS:
        raise ValueError(
            f"Please keep the request under {MAX_PROMPT_CHARACTERS} characters."
        )

    if MODEL_MODE == "mock":
        return PLACEHOLDER_CODE
    if MODEL_MODE != "real":
        raise RuntimeError("MODEL_MODE must be either 'mock' or 'real'.")

    if generate_with_model is None:
        raise RuntimeError("The real model is not initialized.")
    generated_code = _remove_markdown_fences(
        generate_with_model(cleaned_prompt)
    )
    if not generated_code:
        raise RuntimeError("The model returned an empty response.")
    return generated_code
