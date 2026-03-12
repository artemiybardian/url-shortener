from fastapi import FastAPI

from shortener_service.router import router

app = FastAPI(
    title="Shortener Service",
    version="0.1.0",
    root_path="/api/urls",
)

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}
