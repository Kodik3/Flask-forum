from database.core import Connection

class Rating:
    id: int
    user_id: int
    article_id: int
    rating: int
    
    def __init__(self, article_id: int, user_id:str, rating: str):
        self.user_id = user_id
        self.article_id = article_id
        self.rating = rating
    
    @staticmethod
    def create(conn: Connection, user_id: int, article_id: int, rating: int = 0):
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO ratings (user_id, article_id, rating) VALUES (%s, %s, %s)",
                    (user_id, article_id, rating)
                )
                return 0
        except Exception as e:
            print(f"[DB Error] Don't create rating - {e}")
            return f"[DB Error] Don't create rating - {e}"

    @staticmethod
    def select(conn:Connection, request:str = "*", filter_by:str = None, order_by:str = None):
        result = f"SELECT {request} FROM ratings"
        if filter_by:
            result += f" WHERE {filter_by}"
        if order_by:
            result += f" ORDER BY {order_by}"
        with conn.cursor() as cur:
            cur.execute(result)
            return cur.fetchall()
                
    @staticmethod
    def update(conn:Connection, column_name: str, new_value: str, filter_by: str):
        result = f"UPDATE ratings SET {column_name} = {new_value} WHERE {filter_by}"
        with conn.cursor() as cur:
            cur.execute(result)
        return 0

    @staticmethod
    def remove_rating(conn:Connection, filter_by:str):
        result = f"DELETE FROM ratings WHERE {filter_by}"
        with conn.cursor() as cur:
            cur.execute(result)