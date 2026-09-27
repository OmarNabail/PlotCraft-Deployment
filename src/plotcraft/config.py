"""Runtime configuration for PlotCraft."""

import os


MODEL_ID = os.getenv("MODEL_ID", "saeedbenadeeb/NLG_Project")
MODEL_SUBFOLDER = os.getenv("MODEL_SUBFOLDER", "grpo-qwen2.5-3b")
MODEL_MODE = os.getenv("MODEL_MODE", "mock").lower()
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "1024"))
MAX_PROMPT_CHARACTERS = int(os.getenv("MAX_PROMPT_CHARACTERS", "2000"))

SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    (
        "You are PlotCraft, an assistant that converts visualization requests "
        "into executable Python visualization code. Return only the requested "
        "Python code without Markdown fences or additional explanation."
    ),
)
