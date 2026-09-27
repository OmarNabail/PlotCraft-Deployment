import gradio as gr


def generate_plot_code(prompt: str) -> str:
    """Return placeholder plotting code while deployment is being built."""
    if not prompt.strip():
        return "Please enter a plotting request."

    return """import matplotlib.pyplot as plt

categories = ["Model A", "Model B", "Model C"]
scores = [0.78, 0.85, 0.91]

plt.bar(categories, scores)
plt.xlabel("Model")
plt.ylabel("Score")
plt.title("Model Comparison")
plt.show()
"""


demo = gr.Interface(
    fn=generate_plot_code,
    inputs=gr.Textbox(
        label="Plot description",
        placeholder="Create a bar chart comparing three models",
        lines=3,
    ),
    outputs=gr.Code(label="Generated Python code", language="python"),
    title="PlotCraft",
    description=(
        "Generate Matplotlib and TikZ visualization code from "
        "natural-language instructions."
    ),
    examples=[
        ["Create a bar chart comparing three models"],
        ["Create a line chart showing monthly sales"],
    ],
)


if __name__ == "__main__":
    demo.launch()