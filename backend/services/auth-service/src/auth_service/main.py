from fastapi import FastAPI

from auth_service.router import router

app = FastAPI(
    title="Auth Service",
    version="0.1.0",
    root_path="/api/auth",
)

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}
