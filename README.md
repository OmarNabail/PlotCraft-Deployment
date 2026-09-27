---
title: PlotCraft
emoji: 📊
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 6.28.0
python_version: 3.12
app_file: app.py
models:
  - saeedbenadeeb/NLG_Project
short_description: Generate Matplotlib and TikZ code from natural language.
---

# PlotCraft

PlotCraft is a fine-tuned Qwen2.5-3B assistant that generates Matplotlib and
TikZ visualization code from natural-language requests.

The application provides a Gradio interface, a FastAPI service, Docker
packaging, automated tests, and GitHub Actions CI/CD. Generated code is shown
to the user but is not executed on the server.

## Local development

The default `mock` mode does not download the model:

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python -m pytest
python app.py
```

The Hugging Face ZeroGPU Space must set the variable `MODEL_MODE` to `real`.

## API

Run the containerized API with `docker compose up --build`, then open
`http://localhost:8000/docs`. Check its health at
`http://localhost:8000/health`.

## Model

The deployed full model is
[`saeedbenadeeb/NLG_Project/grpo-qwen2.5-3b`](https://huggingface.co/saeedbenadeeb/NLG_Project/tree/main/grpo-qwen2.5-3b).

## Contributors

- Omar Nabail — deployment, API, containerization, testing, and CI/CD
- Saeed Adeeb — model training and dataset development
