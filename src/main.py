import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src.api.routers import editor
from src.core.config import settings

app = FastAPI()
app.include_router(editor.router)

all_cors_origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def hello():
    return HTMLResponse(content="<h1>Hello There!</h1>")


if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)
