from fastapi import APIRouter, HTTPException, Depends
from src.api.service.user_service import UserService
from src.api.models.user import User

router = APIRouter()
user_service = UserService()

@router.get("/user/{user_id}", response_model=User, responses={
    400: {"description": "Bad request, invalid user ID"},
    401: {"description": "Unauthorized access"},
    404: {"description": "User not found"},
})
async def get_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Bad request, invalid user ID")
    
    if not is_authorized():  
        raise HTTPException(status_code=401, detail="Unauthorized access")

    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

def is_authorized():
    return True
