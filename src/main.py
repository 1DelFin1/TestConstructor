import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

allow_origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def hello():
    return HTMLResponse(content='<h1>Hello There!</h1>')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
