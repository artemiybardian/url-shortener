from fastapi import FastAPI

app = FastAPI(
    title="Shortener Service",
    version="0.1.0",
    root_path="/api/urls",
)


@app.get("/health")
async def health():
    return {"status": "ok"}
