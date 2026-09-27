"""FastAPI interface for the PlotCraft generation service."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.plotcraft.service import generate_plot_code


app = FastAPI(
    title="PlotCraft API",
    description="Generate Python visualization code from natural language.",
    version="0.1.0",
)


class GenerationRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=2000)


class GenerationResponse(BaseModel):
    generated_code: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/generate", response_model=GenerationResponse)
def generate(request: GenerationRequest) -> GenerationResponse:
    try:
        code = generate_plot_code(request.prompt)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    return GenerationResponse(generated_code=code)
