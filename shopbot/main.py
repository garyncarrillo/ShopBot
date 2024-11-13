from fastapi import FastAPI
from .routers import main_chat

app = FastAPI()

app.include_router(main_chat.router)

