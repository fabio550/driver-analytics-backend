from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def create_ride():
    return {"status": "ok"}