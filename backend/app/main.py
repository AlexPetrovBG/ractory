from fastapi import FastAPI

app = FastAPI(title="Ra Factory API", version="0.1.0")

@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "ok"} 