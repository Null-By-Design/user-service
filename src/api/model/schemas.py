from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, model_validator

from src.api.model.enum import UserRole, UserStatus


class HealthCheckResponse(BaseModel):
    status: str
    dependencies: dict = {}

    def add_detail(self, key, value):
        self.dependencies[key] = value


class Address(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postalCode: Optional[str] = None


class UserRegistrationRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phoneNumber: Optional[str] = None
    address: Optional[Address] = None
    role: UserRole = UserRole.GUEST
    status: UserStatus = UserStatus.ACTIVE

    @model_validator(mode="before")
    def check_phone_or_email(cls, values):
        if not values.get("phoneNumber") and not values.get("email"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either phone_number or email must be provided.",
            )
        return values


class UserResponse(BaseModel):
    id: int
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phoneNumber: Optional[str] = None
    address: Optional[Address] = None
    role: UserRole
    status: UserStatus
    lastLoginAt: Optional[datetime] = None
    createdAt: datetime
    updatedAt: datetime


class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phoneNumber: Optional[str] = None
    address: Optional[Address] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    
    @model_validator(mode="before")
    def validate_at_least_one_field(cls, values):
        if not any(values.values()):  # Check if all fields are None
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update.",
            )
        return values