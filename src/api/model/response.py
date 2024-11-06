from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from src.api.model.enum import UserRole, UserStatus
from src.api.model.address import Address


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    phoneNumber: str
    address: Address
    role: UserRole
    status: UserStatus
    lastLoginAt: Optional[datetime] = None
    createdAt: datetime
    updatedAt: datetime
