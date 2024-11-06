from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from src.api.model.enum import UserRole, UserStatus


class HealthCheckResponse(BaseModel):
    status: str
    dependencies: dict = {}

    def add_detail(self, key, value):
        self.dependencies[key] = value


class Address(BaseModel):
    street: str
    city: str
    state: str
    country: str
    postalCode: str


class UserRegistrationRequest(BaseModel):
    username: str
    email: EmailStr
    firstName: str
    lastName: str
    phoneNumber: str
    address: Address
    role: UserRole = UserRole.GUEST
    status: UserStatus = UserStatus.ACTIVE


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
