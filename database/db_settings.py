from database.core import Connection

# DataBase settings
HOST = 'localhost'
PORT = 5432
USER = 'postgres'
PASSWORD = 'admin'
DBNAME = 'control'

# Connect
db_conn: Connection = Connection(
    host     = HOST,
    port     = PORT,
    user     = USER,
    password = PASSWORD,
    dbname   = DBNAME
)