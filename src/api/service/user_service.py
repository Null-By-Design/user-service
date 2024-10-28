from repository.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_user(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)