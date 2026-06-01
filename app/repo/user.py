from app.entity.user import User
from app.repo.db_session import DBSession


class UserNotFoundError(Exception):
    pass


class UserRepo:
    def __init__(self, session: DBSession):
        self.session = session

    def login(self, username: str, password: str) -> dict:
        with self.session as session:
            user = session.query(User).filter(
                User.username == username,
                User.password == password
            ).first()
            if not user:
                raise UserNotFoundError("неверный логин или пароль")
            return {
                "id": user.id,
                "username": user.username,
                "fullname": user.fullname,
                "role": user.role.name,
            }
