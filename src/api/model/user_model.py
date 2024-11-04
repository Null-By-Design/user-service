from pydantic import BaseModel
from datetime import datetime

class Address(BaseModel):
    street: str
    city: str
    state: str
    country: str
    postalCode: str

class User(BaseModel):
    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    phoneNumber: str
    address: Address
    role: str
    status: str
    lastLoginAt: datetime
    createdAt: datetime
    updatedAt: datetime
