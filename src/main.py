import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src.api.routers import router
from src.core.config import settings


app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


@app.get("/")
async def hello():
    return HTMLResponse(content="<h1>Hello There!</h1>")


if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)
