from fastapi import APIRouter

router = APIRouter()

@router.get("/internet")
def test_internet():
    return {"message": "Internet route is working!"}