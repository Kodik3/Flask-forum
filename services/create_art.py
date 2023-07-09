# Flask
from datetime import date
# Data Base
from database.db_settings import *
from database.models.articles import Article
from database.models.users import User
from database.models.ratings import Rating
# Services
from services import get


def create_article(data: dict) -> int:
    try:
        today = date.today()
        user = data.get("user")
        content = data.get("content")

        user_id = get.id(User.select(conn=db_conn, request="id", filter_by=f"login = '{user}'"))
        article = Article(content=content, author_id=int(user_id), date_of_creation=str(today))

        if len(article.content) < 1:
            return 2  # если приходит пустой текст

        if len(article.content) > 1000:  # Статья не может быть больше 1000 символов.
            return 1

        # Добавляем статью в таблицу
        create_article_result = Article.create(conn=db_conn, data=article)
        id_article = get.id(Article.select(conn=db_conn, request="id", filter_by=f"content = '{content}'"))

        create_rating = Rating.create(conn=db_conn, user_id=user_id, article_id= id_article)

        # Проверяем, что все создалось.
        if create_article_result == 0 and create_rating == 0:
            return 0  # Все окей...
    except Exception as e:
        print("[Error func] Create article error: {e}")
        return f"[Error func] Create article error: {e}"
