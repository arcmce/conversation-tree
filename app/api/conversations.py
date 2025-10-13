from fastapi import APIRouter

router = APIRouter(prefix="/conversations", tags=["Conversations"])

@router.post("/")
def create_conversation():
    return {"status": "ok", "id": 1}