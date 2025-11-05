from fastapi import FastAPI
from app.api import conversations, turns, health, chat, tree

app = FastAPI(
    title="Conversation Tree API"
)

app.include_router(health.router)
app.include_router(conversations.router)
app.include_router(turns.router)
app.include_router(chat.router)
app.include_router(tree.router)

@app.get("/")
def root():
    return {"message": "Conversation Tree API running"}
