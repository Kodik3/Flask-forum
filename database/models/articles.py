# Data Base
from database.core import Connection


class Article:
    id: int
    content: str
    author_id: int
    date_of_creation: str

    def __init__(self, content: str, author_id: int, date_of_creation: str):
        self.content = content
        self.author_id = author_id
        self.date_of_creation = date_of_creation
    
    @staticmethod
    def create(conn: Connection, data: 'Article'):
        try:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO articles (content, author_id, date_of_creation) VALUES (%s, %s, %s)',
                    (data.content, data.author_id, data.date_of_creation)
                )
            return 0
        except Exception as e:
            print(f"[DB Error] Don't create article - {e}")
            return f"[DB Error] Don't create article - {e}"

    @staticmethod
    def select(conn:Connection, request:str = "*", filter_by:str = None, order_by:str = None):
        result = f"SELECT {request} FROM articles"
        if filter_by:
            result += f" WHERE {filter_by}"
        if order_by:
            result += f" ORDER BY {order_by}"
        with conn.cursor() as cur:
            cur.execute(result)
            return cur.fetchall()
                
    @staticmethod
    def update(conn:Connection, column_name: str, new_value: str, filter_by: str):
        result = f"UPDATE articles SET {column_name} = '{new_value}' WHERE {filter_by}"
        with conn.cursor() as cur:
            cur.execute(result)

    @staticmethod
    def delete(conn:Connection, filter_by:str):
        result = f"DELETE FROM articles WHERE {filter_by}"
        with conn.cursor() as cur:
            cur.execute(result)