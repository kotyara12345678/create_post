from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Posts Microservice")
app.include_router(router)