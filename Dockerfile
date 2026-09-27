FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_MODE=mock

WORKDIR /app

RUN useradd --create-home --uid 10001 plotcraft

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=plotcraft:plotcraft . .

USER plotcraft

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
