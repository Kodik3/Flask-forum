import psycopg2

class Connection:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connection, cls).__new__(cls)
        return cls.instance

    def __init__(self, host:str, port:int, user:str, password:str, dbname:str) -> None:
        self.host= host
        self.port= port
        self.user= user
        self.password= password
        self.dbname= dbname
        self.conn = None
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                dbname=self.dbname
            )
            self.conn.autocommit = True
            print('[SUCCESS] Connection is successful!')
        except Exception as e:
            print(f"[Error] CONNECTION ERROR - {e}")
            
    def create_table(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        login VARCHAR(100) NOT NULL,
                        password VARCHAR(100) NOT NULL CHECK(LENGTH(password) >= 8)
                    );
                    CREATE TABLE IF NOT EXISTS articles (
                        id SERIAL PRIMARY KEY,
                        content VARCHAR(1000) NOT NULL,
                        author_id INTEGER REFERENCES users(id),
                        date_of_creation DATE
                    );
                    CREATE TABLE IF NOT EXISTS comments (
                        id SERIAL PRIMARY KEY,
                        content VARCHAR(500) NOT NULL,
                        comment_date DATE,
                        user_id INTEGER REFERENCES users(id),
                        article_id INTEGER REFERENCES articles(id)
                    );
                    CREATE TABLE IF NOT EXISTS ratings (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER REFERENCES users(id),
                        article_id INTEGER REFERENCES articles(id),
                        rating INTEGER DEFAULT 0
                    );
                ''')
        except Exception as e:
            print(f"[Error] Can't create tables - {e}")

    def cursor(self):
        return self.conn.cursor()
