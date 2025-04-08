from fastapi import FastAPI

from api.v1.endpoints import extract_audio

app = FastAPI(
    title="Audio Extractor API",
    version="1.0.0"
)

app.include_router(extract_audio.router, prefix="/api/v1")
