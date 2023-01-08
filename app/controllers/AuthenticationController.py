import hashlib

from database.exceptions import UserNotExistsException
from utils.TokenHelper import TokenHelper


class AuthenticationController:
    def __init__(self,
                 db_controller):
        self.__db_controller = db_controller

    def validate_token(self,
                       token: str) -> bool:
        email, password = TokenHelper.decode_token(token)

        try:
            password_from_db = self.__db_controller.get_password_by_email(email)
        except UserNotExistsException:
            return False

        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return password_from_db == hashed_password
