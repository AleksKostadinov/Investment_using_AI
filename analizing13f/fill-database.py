import psycopg2
import sys
from sec_api import QueryApi
from decouple import config

# initialize the query API
queryApi = QueryApi(api_key=config("SEC_API_TOKEN"))

# connect to database
conn = psycopg2.connect(
    host=config('POSTGRES_HOST'),
    port="5432",
    database="13f_2023",
    user=config('POSTGRES_USER'),
    password=config('POSTGRES_PASSWORD')
)

def get_13f_filings(start=0, period="2023-06-30"):
    print(f"Getting next 13F batch starting at {start}, {period}")

    query = {
        "query": {
            "query_string": {
                "query": f'formType:"13F-HR" AND NOT formType:"13F-HR/A" AND periodOfReport:"{period}"'
            }
        },
        "from": start,
        "size": "10",
        "sort": [{"filedAt": {"order": "desc"}}],
    }

    response = queryApi.get_filings(query)

    return response["filings"]

def save_to_db(filings):
    cur = conn.cursor()

    for filing in filings:
        if len(filing["holdings"]) == 0:
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
            """,
        )

        filing_values = (
            filing["id"],
            filing["cik"],
            filing["companyName"].upper(),
            filing["periodOfReport"],
        )

        cur.execute(insert_commands[0], filing_values)

        for holding in filing["holdings"]:
            holding_values = (
                filing["id"],
                holding["nameOfIssuer"].upper(),
                holding["cusip"],
                holding["titleOfClass"] if "titleOfClass" in holding else "",
                holding["value"],
                holding["shrsOrPrnAmt"]["sshPrnamt"],
                holding["putCall"] if "putCall" in holding else ""
            )

            cur.execute(insert_commands[1], holding_values)

    cur.close()
    conn.commit()


def fill_database():
    start = 0
    period = sys.argv[1]

    while start < 10000:
        filings = get_13f_filings(start, period)

        if len(filings) == 0:
            break

        save_to_db(filings)
        start = start + 10

    print("Done")


fill_database()
