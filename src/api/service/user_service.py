from repository.user_repository import UserRepository

class UserService:
    def __init__(self, db_url: str):
        self.user_repository = UserRepository(db_url)

    def get_user(self, user_id: int):
        user_data = self.user_repository.get_user_by_id(user_id)
        if user_data:
            return User(**user_data)
        return None
    