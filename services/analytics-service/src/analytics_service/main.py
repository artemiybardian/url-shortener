from fastapi import FastAPI

app = FastAPI(
    title="Analytics Service",
    version="0.1.0",
    root_path="/api/analytics",
)


@app.get("/health")
async def health():
    return {"status": "ok"}
