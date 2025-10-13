from fastapi import FastAPI
from app.api import conversations

app = FastAPI(title="Conversation Tree API")

app.include_router(conversations.router)

@app.get("/")
def root():
    return {"message": "Conversation Tree API running"}
    