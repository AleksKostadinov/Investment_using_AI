import psycopg2
from decouple import config

# connect to database
conn = psycopg2.connect(
    host=config('POSTGRES_HOST'),
    port="5432",
    database="analizing13f20230630",
    user=config('POSTGRES_USER'),
    password=config('POSTGRES_PASSWORD')
)
cur = conn.cursor()

cur.execute("""
SELECT COUNT(DISTINCT cik) as number_of_funds
FROM "filings"
WHERE period_of_report='2023-06-30'
""")

result = cur.fetchone()

cur.close()

print(f"Total number of funds filed for period 2023-06-30:\n{result[0]}")
