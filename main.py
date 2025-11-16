# main.py

import logging
import uvicorn
from fastapi import FastAPI

from api.endpoints import router as api_router
from core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="Summary Evaluation API",
    description="An API to evaluate the quality of a summary against a source transcript using an LLM.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
