from fastapi import APIRouter, HTTPException
from service.user_service import UserService
from models.user import User

router = APIRouter()
user_service = UserService()

@router.get("/user/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
