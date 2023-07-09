# Flask
from flask import session
# Data Base
from database.db_settings import *
from database.models.users import User

def authorize(data: dict) -> int:
    try:
        user = User(login=data.get("login"),password=data.get("password"))
        result_of_authorization = User.authorization_user(conn=db_conn, data=user)
        if isinstance(result_of_authorization, int):
            if result_of_authorization == 0:
                session['logged_in'] = True
                session["login"] = user.login
                return 0
            if result_of_authorization == 1:
                return 1 # Пароль не верный
            if result_of_authorization == 2:
                return 2 # '2' Если такого имени пользователя нет в базе данных.
                
    except Exception as e:
        error = "Authorization Error: " + str(e)
        print(error)
        return {"success": False, "error": error}
    