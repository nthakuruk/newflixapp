import base64


class TokenHelper:
    @staticmethod
    def generate_token(email: str,
                       password: str) -> str:
        credentials = f"{email} {password}"
        return base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    @staticmethod
    def decode_token(token: str) -> list[str, str]:
        return base64.b64decode(token).decode("utf-8").split()


