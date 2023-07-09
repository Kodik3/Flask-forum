import datetime
from database.db_settings import *
from database.all_models import *
from services import get

def append_article() -> list:
    try:
        articles = []
        all_articles = Article.select(conn=db_conn, request="*")
        all_comments = Comment.select(conn=db_conn, request="*")

        for row_articles in all_articles:
            author_name = get.article(User.select(conn=db_conn, request="login", filter_by=f"id = {row_articles[2]}"))
            result_append_articles = {}
            result_append_articles["id_article"] = row_articles[0]
            result_append_articles["content"] = row_articles[1]
            result_append_articles["author_name"] = author_name
            result_append_articles["date_of_creation"] = row_articles[3].strftime('%Y-%m-%d')

            # Комментарии
            comments = []
            if all_comments:
                for row_comments in all_comments:
                    if row_comments[4] == row_articles[0]:  # Проверка соответствия articleId
                        comment_dict = {
                            "id_comment": row_comments[0],
                            "content": row_comments[1],
                            "comment_date": row_comments[2],
                            "user": get.article(User.select(conn=db_conn,request="login", filter_by=f"id = {row_comments[3]}")),
                            "articleId": row_comments[4]
                        }
                        comments.append(comment_dict)
            result_append_articles["comments"] = comments

            # Лайки
            ratings = []
            total_likes = 0  # Инициализация суммы лайков
            all_ratings = Rating.select(conn=db_conn, request="*", filter_by=f"article_id = {row_articles[0]}")  # Получаем все лайки для статьи
            if all_ratings:
                for row_ratings in all_ratings:
                    rating_dict = {
                        "id_rating": row_ratings[0],
                        "user_id": row_ratings[1],
                        "article_id": row_ratings[2]
                    }
                    ratings.append(rating_dict)
                    total_likes += row_ratings[3]  # Добавляем значение лайка к общей сумме
            result_append_articles["total_likes"] = total_likes  # Добавляем сумму лайков в результат

            articles.append(result_append_articles)

        return articles
    except Exception as e:
        print(f"[Error] Append article error - {e}")
        return f"[Error] Append article error - {e}"

