from database.core import Connection


class Comment:
    id: int 
    content: str
    user_id: int
    article_id: int
    comment_date: str

    def __init__(self, content: str, user_id: int, article_id: int, comment_date: str):
        self.content = content
        self.user_id = user_id
        self.article_id = article_id
        self.comment_date = comment_date
    
    @staticmethod
    def create(conn: Connection, data: 'Comment'):
        try:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO comments (content, user_id, article_id, comment_date) VALUES (%s, %s, %s, %s)',
                    (data.content, data.user_id, data.article_id, data.comment_date)
                    )
        except Exception as e:
            print(f"[DB Error] Don't create comment - {e}")
            return f"[DB Error] Don't create comment - {e}"

    @staticmethod
    def select(conn:Connection, request:str = "*", filter_by:str = None, order_by:str = None):
        result = f"SELECT {request} FROM comments"
        if filter_by:
            result += f" WHERE {filter_by}"
        if order_by:
            result += f" ORDER BY {order_by}"
        with conn.cursor() as cur:
            cur.execute(result)
            return cur.fetchall()
                
    @staticmethod
    def remove_rating(conn:Connection, filter_by:str):
        result = f"DELETE FROM comments WHERE {filter_by}"
        with conn.cursor() as cur:
            cur.execute(result)