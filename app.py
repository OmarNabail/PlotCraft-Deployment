import logging

import gradio as gr

from src.plotcraft.service import generate_plot_code


def handle_generation(prompt: str) -> str:
    """Convert application errors into user-friendly messages."""
    try:
        return generate_plot_code(prompt)
    except ValueError as error:
        return str(error)
    except Exception:
        logging.exception("Plot generation failed")
        return "Plot generation failed. Please try again."


demo = gr.Interface(
    fn=handle_generation,
    inputs=gr.Textbox(
        label="Plot description",
        placeholder="Create a bar chart comparing three models",
        lines=3,
    ),
    outputs=gr.Code(
        label="Generated Python code",
        language="python",
    ),
    title="PlotCraft",
    description=(
        "Generate Matplotlib and TikZ visualization code "
        "from natural-language instructions."
    ),
    examples=[
        ["Create a bar chart comparing three models"],
        ["Create a line chart showing monthly sales"],
    ],
)


if __name__ == "__main__":
    # Client-side rendering avoids the extra Node proxy used automatically on
    # Spaces and keeps the ZeroGPU application process simple and reliable.
    demo.launch(ssr_mode=False)
