import logging
from pathlib import Path

import gradio as gr

from src.plotcraft.service import generate_plot_code


EXAMPLE_PROMPTS = [
    [
        "Create a Matplotlib bar chart comparing Model A, Model B, and "
        "Model C with scores 78, 85, and 91. Add labels, a title, and "
        "different colors."
    ],
    [
        "Create a Matplotlib line chart showing monthly sales from January "
        "to June with values 12, 18, 15, 24, 28, and 35. Add markers, axis "
        "labels, a title, and a grid."
    ],
    [
        "Create a Python scatter plot showing the relationship between two "
        "numeric features. Color the points by their y-value and include a "
        "color bar, labels, and a title."
    ],
]

RENDER_PREVIEW_JS = """
(code) => {
    const iframe = document.querySelector("#plotcraft-renderer iframe");
    if (!iframe || !iframe.contentWindow) {
        return [];
    }

    iframe.contentWindow.postMessage(
        {type: "plotcraft:render", code: code || ""},
        "*"
    );
    return [];
}
"""


def handle_generation(prompt: str) -> tuple[str, str]:
    """Generate code and return a clear user-facing status message."""
    try:
        generated_code = generate_plot_code(prompt)
        return generated_code, (
            "Generation complete - review the code, then render it."
        )
    except ValueError as error:
        return "", str(error)
    except Exception:
        logging.exception("Plot generation failed")
        return "", "Plot generation failed. Please try again."


with gr.Blocks(title="PlotCraft") as demo:
    gr.Markdown(
        """
        # PlotCraft

        Turn a plain-language visualization request into executable Python code.

        **How to try it:**
        1. Select an example below or describe your own visualization.
        2. Click **Generate Python Code**.
        3. Wait for the model and review the generated code.
        4. Click **Render Preview** to display the chart in your browser.

        > **Free ZeroGPU demo:** The first request after inactivity may take
        > longer to start, and a short queue is possible during busy periods.
        """
    )

    prompt = gr.Textbox(
        label="Describe your Python visualization",
        placeholder=(
            "Example: Create a Matplotlib bar chart comparing three models "
            "with scores 78, 85, and 91."
        ),
        lines=4,
    )

    gr.Examples(
        examples=EXAMPLE_PROMPTS,
        inputs=prompt,
        label="One-click example prompts",
    )

    generate_button = gr.Button(
        "Generate Python Code",
        variant="primary",
    )
    status = gr.Markdown(
        "Ready - choose an example or enter your own request."
    )

    generated_code = gr.Code(
        label="Generated Python code",
        language="python",
        lines=22,
    )

    render_button = gr.Button("Render Preview", variant="secondary")
    gr.HTML(
        """
        <iframe
            title="PlotCraft browser renderer"
            src="/gradio_api/file=web/renderer.html"
            sandbox="allow-scripts"
            referrerpolicy="no-referrer"
            loading="lazy"
            style="width:100%;min-height:560px;border:0;border-radius:10px;"
        ></iframe>
        """,
        elem_id="plotcraft-renderer",
        container=True,
        padding=True,
    )

    gr.Markdown(
        """
        **Safety notice:** Preview code runs only inside an isolated browser
        worker. It is validated, has no access to the PlotCraft server, and is
        stopped after 10 seconds. Review generated Python before using it
        elsewhere.
        """
    )

    generate_button.click(
        fn=handle_generation,
        inputs=prompt,
        outputs=[generated_code, status],
        api_name="generate_python_code",
    )
    prompt.submit(
        fn=handle_generation,
        inputs=prompt,
        outputs=[generated_code, status],
        api_name=False,
    )
    render_button.click(
        fn=None,
        inputs=generated_code,
        outputs=None,
        js=RENDER_PREVIEW_JS,
        queue=False,
        api_visibility="private",
    )

demo.queue(default_concurrency_limit=1, max_size=10)


if __name__ == "__main__":
    # Client-side rendering avoids the extra Node proxy used automatically on
    # Spaces and keeps the ZeroGPU application process simple and reliable.
    demo.launch(
        ssr_mode=False,
        allowed_paths=[str(Path(__file__).parent / "web")],
    )
