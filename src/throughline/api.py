"""FastAPI application for Throughline."""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

# Load .env at import time so settings are available to all endpoints.
load_dotenv()

app = FastAPI(
    title="Throughline",
    description="Film recommendations by emotional trajectory.",
    version="0.1.0",
)


class HealthResponse(BaseModel):
    """Response shape for the health check endpoint."""

    status: str
    version: str
    anthropic_key_loaded: bool


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Confirm the service is running and config is loaded."""
    return HealthResponse(
        status="ok",
        version="0.1.0",
        anthropic_key_loaded=bool(os.getenv("ANTHROPIC_API_KEY")),
    )