from database.helpers.QueryHelper import QueryHelper
from database.exceptions import UserExistsException


class DataBaseController:

    @QueryHelper.query
    def create_user(self,
                    first_name,
                    last_name,
                    phone_number,
                    email,
                    password,
                    cur=None
                    ):
        if self.get_password_by_email(email):
            raise UserExistsException

        query = f"INSERT INTO `users`" \
                f" (`name`,`surname`,`phone_number`,`email`," \
                f" `password`) " \
                f"VALUES ('{first_name}', '{last_name}', '{phone_number}'," \
                f" '{email}', '{password}')"

        cur.execute(query)

    @QueryHelper.query
    def get_user_id_by_email(self,
                             email,
                             cur=None
                             ):
        query = f"SELECT `id` FROM `users`" \
                f" WHERE `email` = '{email}'"

        cur.execute(query)
        row = cur.fetchone()
        return row["id"]

    @QueryHelper.query
    def get_email_by_user_id(self,
                             user_id,
                             cur=None
                             ):
        query = f"SELECT `email` FROM `users`" \
                f" WHERE `id` = '{user_id}'"

        cur.execute(query)
        row = cur.fetchone()
        return row["email"]

    @QueryHelper.query
    def get_password_by_email(self,
                              email,
                              cur=None
                              ):
        query = f"SELECT `password` FROM `users`" \
                f" WHERE `email` = '{email}'"

        cur.execute(query)
        row = cur.fetchone()
        return row["password"] if row else row
