from typing import Optional

from fastapi import HTTPException, status
from psycopg2 import errors
from psycopg2.extras import DictCursor

from src.api.config.database import DatabasePool
from src.api.mapper.user_mapper import UserMapper
from src.api.model.domain import Address, User
from src.api.model.schemas import UserUpdateRequest


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

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Fetch a user from the database by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            Optional[User]: The user object if found, else None.
        """
        try:
            with DatabasePool.get_connection() as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    query = """
                        SELECT id, username, email, first_name, last_name, phone_number,
                               address_id, role, status, last_login_at, created_at, updated_at
                        FROM "user"
                        WHERE id = %s;
                    """
                    cur.execute(query, (user_id,))
                    result = cur.fetchone()

                    if result:
                        address = self._get_address(cur, result["address_id"])
                        return UserMapper.build_user_object(result, address)
                    return None

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching user from database: {str(e)}",
            )

    def _get_address(self, cur, id: int) -> Optional[Address]:
        """Fetch the address for a user by address ID."""
        address_query = """
            SELECT street, city, state, postal_code, country
            FROM address
            WHERE id = %s;
        """
        cur.execute(address_query, (id,))
        address_result = cur.fetchone()
        if address_result:
            return Address(
                street=address_result["street"],
                city=address_result["city"],
                state=address_result["state"],
                postal_code=address_result["postal_code"],
                country=address_result["country"]
            )
        return None
    
    def update_user(self, user_id: int, updated_user_data: UserUpdateRequest) -> Optional[User]:
     
        try:
            with DatabasePool.get_connection() as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    existing_user = self.get_user(user_id)
                    if not existing_user:
                        return None

                    if updated_user_data.address:
                        if existing_user.address:
                            self._update_address(cur, existing_user.address.id, updated_user_data.address)
                        else:
                            address_id = self._insert_address(cur, updated_user_data.address)
                            address_query = """
                                UPDATE "user"
                                SET address_id = %s, updated_at = NOW()
                                WHERE id = %s;
                            """
                        cur.execute(address_query, (address_id, user_id))
                        
                    # Update user fields dynamically
                    user_query = """
                        UPDATE "user"
                        SET 
                            username = %s,
                            email = %s,
                            first_name = %s,
                            last_name = %s,
                            phone_number = %s,
                            role = %s,
                            status = %s,
                            updated_at = NOW()
                        WHERE id = %s
                        RETURNING id, username, email, first_name, last_name, phone_number, address_id,
                                  role, status, last_login_at, created_at, updated_at;
                    """
                    user_values = (
                        updated_user_data.username,
                        updated_user_data.email,
                        updated_user_data.first_name,
                        updated_user_data.last_name,
                        updated_user_data.phoneNumber,
                        updated_user_data.role.value if updated_user_data.role else None,
                        updated_user_data.status.value if updated_user_data.status else None,
                        user_id,
                    )
                    cur.execute(user_query, user_values)
                    updated_user_result = cur.fetchone()

                    updated_address = None
                    if updated_user_result["address_id"]:
                        updated_address = self._get_address(cur, updated_user_result["address_id"])

                    return UserMapper.build_user_object(updated_user_result, updated_address)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating user: {str(e)}",
            )

    def update_address(self, cur, address_id: int, address_data: Address):
        address_query = """
        UPDATE address
        SET street = %s, city = %s, state = %s, postal_code = %s, country = %s
        WHERE id = %s
        RETURNING id, street, city, state, postal_code, country;
    """
        address_values = (
            address_data.street,
            address_data.city,
            address_data.state,
            address_data.postal_code,
            address_data.country,
            address_id,
        )
        cur.execute(address_query, address_values)
        return cur.fetchone()
   


