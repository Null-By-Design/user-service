from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies.provider import get_user_service
from src.api.mapper.user_mapper import UserMapper
from src.api.model.schemas import UserRegistrationRequest, UserResponse
from src.api.service.user_service import UserService


router = APIRouter(prefix="/api/v1")


@router.post(
    "/user",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User registered successfully"},
        400: {"description": "Bad request, invalid registration data"},
    },
)
async def register_user(
    request: UserRegistrationRequest,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        # Convert request to domain model
        user = UserMapper.to_domain(request)

        # Call service layer
        created_user = await user_service.register_user(user)

        # Convert domain model to response
        return UserMapper.to_response(created_user)

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid registration data: {str(e)}",
        )

@router.get(
    "/user/{id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "User not found"}},
)

async def get_user(
    id: int,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        # Call service to get user by ID
        user = await user_service.get_user(id)
        if not user: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"            
            )

        # Convert domain model to response
        return UserMapper.to_response(user)

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
