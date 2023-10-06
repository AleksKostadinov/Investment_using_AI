from sec_api import QueryApi
import pandas as pd
import psycopg2
from decouple import config

# connect to database
conn = psycopg2.connect(
    host=config('POSTGRES_HOST'),
    port="5432",
    database="13f_full",
    user=config('POSTGRES_USER'),
    password=config('POSTGRES_PASSWORD')
)
# create a cursor
cur = conn.cursor()

# initialize the query API
queryApi = QueryApi(api_key=config("SEC_API_TOKEN"))

def get_13f_filings(start=0):
    print(f"Getting next 13F batch starting at {start}")

    query = {
      "query": { "query_string": {
          "query": "formType:\"13F-HR\" AND NOT formType:\"13F-HR/A\" AND periodOfReport:\"2023-06-30\""
        } },
      "from": start,
      "size": "10000",
      "sort": [{ "filedAt": { "order": "desc" } }]
    }

    response = queryApi.get_filings(query)

    return response['filings']

# fetch the 10 most recent 13F filings
filings_batch = get_13f_filings()

# load all holdings of the first 13F filing into a pandas dataframe
holdings_example = pd.json_normalize(filings_batch[0]['holdings'])


def save_to_db(filings):
    cur = conn.cursor()

    for filing in filings:
        if len(filing['holdings']) == 0:
            continue

        insert_commands = (
            """
                INSERT INTO filings (
                    filing_id,
                    cik,
                    filer_name,
                    period_of_report
                )
                VALUES (%s, %s, %s, %s)
            """,
            """
                INSERT INTO holdings (
                    filing_id,
                    name_of_issuer,
                    cusip,
                    title_of_class,
                    value,
                    shares,
                    put_call
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        )

        filing_values = (
            filing['id'],
            filing['cik'],
            filing['companyName'].upper(), # convert all names to upper case to make unique search easier
            filing['periodOfReport']
        )

        cur.execute(insert_commands[0], filing_values)

        for holding in filing['holdings']:
            holding_values = (
                filing['id'],
                holding['nameOfIssuer'].upper(), # convert all names to upper case to make unique search easier
                holding['cusip'],
                holding['titleOfClass'],
                holding['value'],
                holding['shrsOrPrnAmt']['sshPrnamt'],
                holding['putCall'] if 'putCall' in holding else '',
            )

            cur.execute(insert_commands[1], holding_values)

    cur.close()
    conn.commit()

filings_batch = get_13f_filings()
save_to_db(filings_batch)

