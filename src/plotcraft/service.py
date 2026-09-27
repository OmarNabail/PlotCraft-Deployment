PLACEHOLDER_CODE = """import matplotlib.pyplot as plt

categories = ["Model A", "Model B", "Model C"]
scores = [0.78, 0.85, 0.91]

plt.bar(categories, scores)
plt.xlabel("Model")
plt.ylabel("Score")
plt.title("Model Comparison")
plt.show()
"""


def generate_plot_code(prompt: str) -> str:
    """Generate plotting code from a natural-language request."""

    cleaned_prompt = prompt.strip()

    if not cleaned_prompt:
        raise ValueError("Please enter a plotting request.")

    return PLACEHOLDER_CODE