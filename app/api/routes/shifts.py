from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def create_shift():
    return {"status": "ok"}