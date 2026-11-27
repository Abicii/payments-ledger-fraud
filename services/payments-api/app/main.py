from fastapi import FastAPI

app = FastAPI(title="Payments API", version="0.1.0")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}
