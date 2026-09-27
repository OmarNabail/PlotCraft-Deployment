---
title: PlotCraft
sdk: gradio
sdk_version: 6.28.0
python_version: 3.12
app_file: app.py
models:
  - PlotCraft
short_description: Generate Python visualization code from natural language.
---

# PlotCraft

[![CI](https://github.com/OmarNabail/PlotCraft-Deployment/actions/workflows/ci.yml/badge.svg)](https://github.com/OmarNabail/PlotCraft-Deployment/actions/workflows/ci.yml)
[![Deployment](https://github.com/OmarNabail/PlotCraft-Deployment/actions/workflows/sync-to-hub.yml/badge.svg?branch=main)](https://github.com/OmarNabail/PlotCraft-Deployment/actions/workflows/sync-to-hub.yml)

PlotCraft is a fine-tuned Qwen2.5-3B assistant that converts natural-language
requests into executable Python visualization code. This repository contains
the Gradio application, FastAPI service, Docker configuration, automated tests,
and GitHub Actions deployment pipeline.

**[Try the live ZeroGPU demo](https://huggingface.co/spaces/omargam220/PlotCraft)**

Generated code is displayed for review and can be rendered as a PNG inside an
isolated browser worker. Generated code is never executed on the server.

## Use the live application

1. Open the live demo.
2. Describe the Python visualization you want.
3. Select **Generate Python Code**.
4. Review the generated Python code.
5. Select **Render Preview** to display the chart in the browser.
6. Copy the code if you want to use it in your own project.

Example request:

```text
Create a Matplotlib bar chart with categories A, B, C and values 2, 5, 3.
```

## Run locally

Create and activate a virtual environment in Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Install the dependencies and start the application:

```bash
pip install -r requirements.txt
python app.py
```

Local execution uses the lightweight mock mode by default, so it does not
download the production model.

Run the tests with:

```bash
python -m pytest
```

## Run the API with Docker

Build and start the container:

```bash
docker compose up --build
```

Open the interactive API documentation at:

```text
http://localhost:8000/docs
```

Available endpoints:

- `GET /health` checks whether the service is running.
- `POST /generate` accepts a prompt and returns generated Python code.

Stop the container with:

```bash
docker compose down
```
