# Python
from datetime import date
# Data Base
from database.db_settings import *
from database.models.comments import Comment
from database.models.users import User
# Services
from services import get



def create_comm(data: dict) -> int:
    try:
        today = date.today()
        user = data.get("user")
        user_id = get.id(User.select(conn=db_conn, request="id", filter_by=f"login = '{user}'"))
        comment = Comment(content=data.get("content"), user_id=int(user_id), article_id=data.get("articleId"), comment_date = today)   

        if comment.content is None:
            return 2 # коментарий не может быть пустой.

        if len(comment.content) > 500:
            return 1 # коментарий не может быть больше 500 символов.

        if comment.article_id is None:
            return 3 # 

        create_comment_res = Comment.create(conn=db_conn, data=comment)
        return 0  # Все ок...
    except Exception as e:
        print(f"[Error] Create article error: {e}")
        return f"[Error] Create article error: {e}"