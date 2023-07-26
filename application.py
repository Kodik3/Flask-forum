# Flask
from flask import Flask, render_template, json, url_for, redirect, request, session, jsonify
# Data Base
from database.db_settings import *
from database.all_models import *
# Services
from services.interface import *

# App
app: Flask = Flask(__name__, static_folder='static')

# PAGES
#---------------------------------------------------------

# Main.
@app.route("/main", methods=['GET'])
def main_page():
    articles = append_article() # Берем 'dict' с сохронеными статьями, комментариями, оценками.
    profile = session.get("login") # Берем имя пользователя в сессии.
    return render_template("main.html", user_profile=profile, articles=articles)

# Registration.
@app.route("/registration", methods=['GET'])
def registration_page():
    if not session.get("login") is None:
        return redirect(url_for("main_page"))
    return render_template("registration.html")

# Login.
@app.route("/authorization", methods=['GET'])
def login_page():
    if not session.get("login") is None:
        return redirect(url_for("main_page"))
    return render_template("login.html")

# Logout (clear session).
@app.route("/logout", methods=["GET"])
def logout():
    session.clear() # Очищаем данные сеанса.
    return redirect(url_for("main_page"))

# Create articles.
@app.route("/create_articles", methods=['GET'])
def page_create_articles():
    if session.get("login") is None:
        return render_template("login.html")
    return render_template("create_articles.html", user_profile=session.get("login"))

#---------------------------------------------------------
# Функции
#---------------------------------------------------------

# Registration.
@app.route("/api/v1/registration", methods=["POST"])
def registration():
    try:
        data = request.get_json() # получаем данные от js.
        result = registrate(data=data) # отпровляем эти данные в функцию 'registrate'.
        return json.dumps(result) # возврощаем int'овое значение в js.
    except Exception as ex:
        print(f"[Server Error] Registration error - {ex}")
        return f"[Server Error] Registration error - {ex}"

# Authorization.
@app.route("/api/v1/authorization", methods=["GET", "POST"])
def login():
    try:
        data = request.get_json() # получаем данные от js.
        result = authorize(data=data) # отпровляем эти данные в функцию 'authorize'.
        return json.dumps(result) # возврощаем int'овое значение в js.
    except Exception as ex:
        print(f"[Server Error] Authorization error - {ex}")
        return f"[Server Error] Authorization error - {ex}"

# Articles.
@app.route("/api/v1/create_articles_app", methods=["GET","POST"])
def create_articles_app():
    try:
        data = request.get_json() # получаем данные от js.
        data["user"]= session.get("login") # Получаем name пользователя и добовляем в data.
        result = create_article(data=data) # отпровляем эти данные в функцию 'create_article'.
        return json.dumps(result) # возврощаем int'овое значение в js.
    except Exception as ex:
        print(f"[Server Error] Create article error - {ex}")
        return f"[Server Error] Create article error - {ex}"

# Comments.
@app.route("/api/v1/add_comment", methods=["GET", "POST"])
def add_comment_app():
    try:
        if session.get("login") is None: # Проверка находится ли пользователь в аккаунте.
            error = "Your account is None"
            return {"Create comment error" : error}
        data = request.get_json() # получаем данные от js.
        data["user"] = session.get("login") # Получаем name пользователя и добовляем в data.
        result = create_comm(data=data) # отпровляем эти данные в функцию 'create_comm'.
        return json.dumps(result)
    except Exception as ex:
        print(f"[Server Error] Create comment error - {ex}")
        return f"[Server Error] Create comment error - {ex}"

# Likes.
@app.route("/api/v1/update_like_count", methods=["GET", "POST"])
def update_like_count_app():
    try:
        if session.get("login") is None: # Проверка находится ли пользователь в аккаунте.
            return redirect(url_for("login_page"))
        data = request.get_json()
        data["user"] = session.get("login")
        result = create_rating(data=data)
        return jsonify(result)
    except Exception as ex:
        print(f"[Server Error] Create rating error - {ex}")
        return f"[Server Error] Create rating error - {ex}"

#---------------------------------------------------------

if __name__ == '__main__':
    db_conn.create_table() # создание таблиц в DataBase.
    app.run() # Запуск сервера.
