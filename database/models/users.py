from database.core import Connection
# Services
from services import get


class User:
    id: int 
    login: str # имя
    password: str # пароль

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

    # Reg... user
    @staticmethod
    def registrate_user(conn: Connection, data: 'User') -> int:
        # Проверка на существуещего пользователя.
        with conn.cursor() as cur:
            cur.execute('SELECT id FROM users WHERE login=%s',(data.login,))
            
            if cur.fetchone(): # Возвращает '3', когда пользователь существует.
                return 3

        with conn.cursor() as cur:
            cur.execute('INSERT INTO users (login, password) VALUES (%s, %s)',
                        (data.login, data.password))
        return 0  # Все хорошо.

    @staticmethod
    def authorization_user(conn: Connection, data: 'User') -> int:
        with conn.cursor() as cur:
            # id имени пользователя.
            cur.execute('SELECT id FROM users WHERE login=%s', (data.login,))
            result_id_name: int = get.text(cur.fetchone())
            # Берем пароль от пользователя
            cur.execute('SELECT password FROM users WHERE id=%s', (result_id_name,))
            user_pasword: str = get.text(cur.fetchone())

            if result_id_name: # проверяем существует ли пользователь.
                if user_pasword == data.password: # Проверяем подходит пароль к юзеру
                    return 0 # '0' Все хорошо Пользователь с таки паролем существует.
                return 1 # '1' Пароль не верный
            return 2 # '2' Если такого имени пользователя нет в базе данных.

# DataBase функции.
#--------------------------------------------------------------------------------------
    @staticmethod
    def create(login: str, password:str, conn: Connection):
        with conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO users (login, password)
                VALUES ('{login}', '{password}')
                """)

    @staticmethod
    def select(conn:Connection, request:str = "*", filter_by:str = None, order_by:str = None):
        result = f"SELECT {request} FROM users"
        if filter_by:
            result += f" WHERE {filter_by}"
        if order_by:
            result += f" ORDER BY {order_by}"
        with conn.cursor() as cur:
            cur.execute(result)
            return cur.fetchall()
                
    @staticmethod
    def update(conn:Connection, column_name: str, new_value: str, filter_by: str):
        result = f"UPDATE users SET {column_name} = '{new_value}' WHERE {filter_by}"
        with conn.cursor() as cur:
            cur.execute(result)

    @staticmethod
    def delete(conn:Connection, filter_by:str):
        result = f"DELETE FROM users WHERE {filter_by}"
        with conn.cursor() as cur:
            cur.execute(result)
#--------------------------------------------------------------------------------------
