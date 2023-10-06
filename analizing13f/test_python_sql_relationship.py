import psycopg2
from decouple import config

# connect to database
conn = psycopg2.connect(
    host=config('POSTGRES_HOST'),
    port="5432",
    database="analizing13f",
    user=config('POSTGRES_USER'),
    password=config('POSTGRES_PASSWORD')
)
# create a cursor
cur = conn.cursor()

# execute a statement
cur.execute('SELECT version()')

# display the PostgreSQL database server version
db_version = cur.fetchone()

print('PostgreSQL database version:')
print(db_version)

# close the communication with the PostgreSQL
cur.close()
