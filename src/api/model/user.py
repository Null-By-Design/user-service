from datetime import datetime, timezone
from typing import Optional

from src.api.model.enum import UserRole, UserStatus
from src.api.model.address import Address


class User:
    def __init__(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        address: Address,
        role: UserRole = UserRole.GUEST,
        status: UserStatus = UserStatus.ACTIVE,
        id: Optional[int] = None,
        last_login_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
        self.role = role
        self.status = status
        self.last_login_at = last_login_at
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)
