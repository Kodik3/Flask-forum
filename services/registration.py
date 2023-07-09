# Flask
from flask import session
# Data Base
from database.db_settings import *
from database.models.users import User

# Registration.
def registrate(data: dict) -> int:
    try:
        user = User(login=data.get("login"), password=data.get("password")) # Создание модели пользователя.
        # Ошибки
        if len(user.password) < 8: # '2' Если пароль не подходит
            return 2 

        if user.password != data.get("rpassword"): # '1' Если повторный пароль не ровняется паролю
            return 1 
        
        if data.get('login') == "": # '4' если пользователь не ввел имя.
            return 4 

        result_of_registration = User.registrate_user(conn=db_conn, data=user) # Добовляем пользователя в DataBase.
        if isinstance(result_of_registration, int): # Проверка на то что результат евляется int'овым значением.
            if result_of_registration == 0:
                session['logged_in'] = True
                session["login"] = user.login # Добовляем пользователя в сессию.
                return 0 # '0' Если все успешно

            if result_of_registration == 3:
                return 3 # Возвращает '3', когда пользователь существует.
    except Exception as e:
        print(f"[Error func.] Registration Error: {e}")
