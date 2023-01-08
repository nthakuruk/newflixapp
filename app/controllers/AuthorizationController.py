import hashlib

from database.exceptions import UserExistsException
from controllers.exceptions import LoginRequired


class AuthorizationController:
    def __init__(self,
                 db_controller):
        self.__db_controller = db_controller

    def register(self,
                 first_name: str,
                 last_name: str,
                 phone_number: str,
                 email: str,
                 password: str):
        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        try:
            self.__db_controller.create_user(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email,
                password=hashed_password
            )
        except UserExistsException:
            raise LoginRequired

    def login(self,
              email: str,
              password: str) -> bool:
        password_from_db = self.__db_controller.get_password_by_email(email)
        if not password_from_db:
            return False
        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return password_from_db == hashed_password
