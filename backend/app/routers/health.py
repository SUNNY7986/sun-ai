from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "Sun AI is running"}