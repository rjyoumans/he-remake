from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def test_internet():
    return {"message": "Internet route is working!"}