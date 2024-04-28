from extensions import mysql
from MySQLdb.cursors import DictCursor

from abc import ABC, abstractmethod

class DatabaseModel(ABC):
    def __init__(self, cursor):
        self.cursor = cursor

    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def get(self):
        pass

class Birthday(DatabaseModel):
    def __init__(self, name, date, account_id, cursor):
        super().__init__(cursor)
        self.name = name
        self.date = date
        self.account_id = account_id

    def insert(self):
        self.cursor.execute('INSERT INTO birthdays (name, date, account_id) VALUES (%s, %s, %s)', (self.name, self.date, self.account_id,))
        mysql.connection.commit()

    def get(account_id):
        cursor = mysql.connection.cursor(cursorclass=DictCursor)
        cursor.execute('SELECT * FROM birthdays WHERE account_id = %s', (account_id,))
        return cursor.fetchall()

class Account(DatabaseModel):
    def __init__(self, email, password, cursor):
        super().__init__(cursor)
        self.email = email
        self.password = password

    def insert(self):
        self.cursor.execute('INSERT INTO accounts (email, password) VALUES (%s, %s)', (self.email, self.password,))
        mysql.connection.commit()

    def get(email, password):
        cursor = mysql.connection.cursor(cursorclass=DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password,))
        return cursor.fetchone()

class DatabaseService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseService, cls).__new__(cls)
        return cls._instance

    def __create_cursor(self):
        return mysql.connection.cursor(cursorclass=DictCursor)

    def insert_birthday(self, name, date, account_id):
        birthday = Birthday(name, date, account_id, self.__create_cursor())
        birthday.insert()

    def get_birthdays(self, account_id):
        return Birthday.get(account_id)

    def get_account(self, email, password):
        return Account.get(email, password)

    def insert_account(self, email, password):
        account = Account(email, password, self.__create_cursor())
        account.insert()
