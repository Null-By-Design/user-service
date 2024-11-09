from typing import Optional

from fastapi import HTTPException, status
from psycopg2 import errors
from psycopg2.extras import DictCursor

from src.api.model.domain import Address, User
from src.api.config.database import DatabasePool
from src.api.mapper.user_mapper import UserMapper


class UserRepository:
    def check_db_connection(self):
        """
        Attempts to establish a connection to the database and execute a simple
        query.

        Returns a string indicating the outcome of the check. If the check
        succeeds, the string will be "Connected". If the check fails, the
        string will be a description of the error that occurred.

        :return: A string indicating the health of the database connection.
        :rtype: str
        """
        try:
            with DatabasePool.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    return "Connected"
        except Exception as e:
            return f"Failed to connect to database: {str(e)}"

    def save(self, user: User) -> Optional[User]:
        """
        Saves a user to the database.

        :param user: The user to save.
        :type user: User
        :return: The saved user, or None if the save failed.
        :rtype: Optional[User]
        :raises Exception: if an error occurs while saving the user.
        """
        try:
            with DatabasePool.get_connection() as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    address_id = (
                        None
                        if user.address is None
                        else self._insert_address(cur, user.address)
                    )
                    result = self._insert_user(cur, user, address_id)
                    conn.commit()

                    return (
                        UserMapper.build_user_object(result, user.address)
                        if result
                        else None
                    )

        except errors.UniqueViolation as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User already exists: {str(e)}",
            )
        except Exception as e:
            raise Exception(f"Error saving user: {str(e)}")

    def _insert_address(self, cur, address: Address) -> int:
        """Inserts the address and returns the generated address ID."""
        address_query = """
            INSERT INTO address (street, city, state, postal_code, country)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """
        address_values = (
            address.street,
            address.city,
            address.state,
            address.postal_code,
            address.country,
        )
        cur.execute(address_query, address_values)
        return cur.fetchone()["id"]

    def _insert_user(self, cur, user: User, address_id: int) -> dict:
        """Inserts the user and returns the database result row."""
        user_query = """
            INSERT INTO "user" 
            (username, email, first_name, last_name, phone_number, 
            address_id, role, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, username, email, first_name, last_name, 
                    phone_number, address_id, role, status, 
                    last_login_at, created_at, updated_at;
        """
        user_values = (
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            user.phone_number,
            address_id,
            user.role.value,
            user.status.value,
            user.created_at,
            user.updated_at,
        )
        cur.execute(user_query, user_values)
        return cur.fetchone()
