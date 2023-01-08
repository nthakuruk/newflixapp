import pymysql

from configs.Config import Config


class DataBaseConnection:
    __instances: dict = {'db_connection': None}
    __config = Config()

    def __new__(cls,
                *args,
                **kwargs) -> pymysql.connect:
        if not cls.__instances['db_connection']:
            cls.__instances['db_connection'] = \
                pymysql.connect(host=cls.__config.DB_HOST,
                                user=cls.__config.DB_USER,
                                password=cls.__config.DB_PASSWORD,
                                database=cls.__config.DB_NAME,
                                port=cls.__config.DB_PORT,
                                cursorclass=pymysql.cursors.DictCursor)
        return cls.__instances['db_connection']
