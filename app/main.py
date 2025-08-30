from fastapi import FastAPI
from api.v1.api import api_router

app = FastAPI(
    title="Personal Finance Tracker API",
    description="A JWT-authenticated API for tracking personal finances",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Personal Finance Tracker API"}