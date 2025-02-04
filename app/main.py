# app/main.py
import uvicorn
from fastapi import FastAPI
from app.routes import router as vk_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="VK Callback Bot")
app.include_router(vk_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8088, reload=True)