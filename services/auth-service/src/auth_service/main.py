from fastapi import FastAPI

app = FastAPI(
    title="Auth Service",
    version="0.1.0",
    root_path="/api/auth",
)


@app.get("/health")
async def health():
    return {"status": "ok"}
