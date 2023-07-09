# Data Base
from database.db_settings import *
from database.models.ratings import Rating
from database.models.users import User
#Services
from services import get



def create_rating(data: dict) -> int:
    try:
        # Берем id(пользователя) и id(статьи)
        username = data.get("user")
        user_id = get.id(User.select(conn=db_conn, request="id", filter_by=f"login = '{username}'"))
        article_id = data.get("articleId")

        lst_users_id = []

        if username is None:
            return 1 # Пользователь не авторизован

        rating_check = get.id(Rating.select(conn=db_conn, request="user_id", filter_by=f"article_id = {article_id}"))
        lst_users_id.append(rating_check)
        if user_id in lst_users_id:
            Rating.remove_rating(conn=db_conn, filter_by=f"user_id = {user_id} AND article_id = {article_id}")
            return 2  # Лайк отменен

        
        result=Rating.create(conn=db_conn, user_id=user_id, article_id=article_id, rating=1)
        if result == 0:
            return 0  # Лайк поставлен.

    except Exception as e:
        raise Exception(f"[FUNC.Error] Create rating error: {e}")