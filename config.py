import sqlite3


class Config:
    def __init__(self):
        self.create_data_table()

    def create_connection(self):
        return sqlite3.connect('home_service.db')

    def create_data_table(self):
        self.execute('CREATE TABLE IF NOT EXISTS `data` ('
                     'uid INTEGER PRIMARY KEY AUTOINCREMENT,'
                     '`name` VARCHAR(128) NOT NULL,'
                     '`value` VARCHAR(2048) NOT NULL);')

    def execute(self, req, *args, commit=True, fetch_one=False, fetch_all=False, connection=None):
        if not connection:
            connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(req, args)
        data = None
        if commit:
            connection.commit()
        if fetch_one:
            data = cursor.fetchone()
        if fetch_all:
            data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data

    def is_init(self, connection):
        data = self.execute('SELECT * FROM `data`', fetch_all=True, connection=connection)
        return len(data) == 0

    def get_settings(self, connection):
        data = self.execute('SELECT `name`,`value` FROM `data`', fetch_all=True, connection=connection)
        d = {}
        for i in data:
            d.update({i[0]: i[1]})
        return d

    def inset_in_data(self, **kwargs):
        for i, k in kwargs.items():
            self.execute('INSERT INTO `data` (`name`,`value`) VALUES (?,?)', i, k)

    def apply_settings(self, language: str, path: str, admin_login: str, admin_password: str, connection=None):
        self.inset_in_data(language=language, path=path, admin_login=admin_login, admin_password=admin_password)


con = Config()
