import pandas as pd
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

conn.commit()
cur = conn.cursor()

cur.execute("""
SELECT shares, holdings.cusip, security_name, ticker, period_of_report, holdings.filing_id
FROM "holdings"
INNER JOIN filings
ON filings.filing_id = holdings.filing_id
INNER JOIN holding_infos
ON holdings.cusip = holding_infos.cusip
WHERE (period_of_report = '2023-06-30' or period_of_report = '2023-03-31') and cik = '1067983'
""")

rows = cur.fetchall()

cur.close()

buffet_holdings = pd.DataFrame(rows, columns=['Shares',
                                              'CUSIP',
                                              'SecurityName',
                                              'Ticker',
                                              'PeriodOfReport',
                                              'FilingId'])
