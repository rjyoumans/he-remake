from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/")
def test_auth():
    return {"message": "Authentication successful"}