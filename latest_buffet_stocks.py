import json
import requests
import psycopg2
from psycopg2 import sql
from decouple import config


token = config("SEC_API_TOKEN")

json_request_data = {
    "query": {
        "query_string": {
            "query": "formType:\"13F\" AND holdings.cik:1318605"
        }
    },
    "from": "0",
    "size": "20",
    "sort": [{"filedAt": {"order": "desc"}}]
}

response = requests.post(
    "https://api.sec-api.io?token=" + token, json=json_request_data)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    json_data = response.json()

    holdings_data = []
    for filing in json_data["filings"]:
        for holding in filing["holdings"]:
            try:
                ticker = holding["ticker"]
            except Exception as e:
                print(e)
                ticker = holding["shrsOrPrnAmt"]["sshPrnamtType"]
            name_of_issuer = holding["nameOfIssuer"]
            try:
                cik = holding["cik"]
            except Exception as e:
                print(e)

            value = holding["value"]
            shrs_or_prn_amt = holding["shrsOrPrnAmt"]["sshPrnamt"]

            # Append the extracted data to the list
            holdings_data.append({
                "nameOfIssuer": name_of_issuer,
                "ticker": ticker,
                "value": value,
                "shrsOrPrnAmt": shrs_or_prn_amt,
                "cik": cik
            })

else:
    print(f"API request failed with status code: {response.status_code}")


# Database connection parameters
try:
    conn = psycopg2.connect(
        host=config('POSTGRES_HOST'),
        port="5432",
        database=config('POSTGRES_DB'),
        user=config('POSTGRES_USER'),
        password=config('POSTGRES_PASSWORD')
    )

    with conn:
        with conn.cursor() as cur:
            # SQL statement for inserting data
            insert_query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS latest_buffet_stocks(
                    "id" serial PRIMARY KEY,
                    "name" VARCHAR(100),
                    ticker VARCHAR(10),
                    value NUMERIC,
                    shares NUMERIC,
                    cik INTEGER DEFAULT NULL
                );

                INSERT INTO latest_buffet_stocks ("name", ticker, value, shares, cik)
                VALUES (%s, %s, %s, %s, %s);
            """)

            # Insert data into the database
            for item in holdings_data:
                # Convert empty strings to 0 for cik
                cik = item["cik"] if item["cik"] != '' else None
                cur.execute(insert_query, (item["nameOfIssuer"], item["ticker"],
                            item["value"], item["shrsOrPrnAmt"], cik))
                print(
                    f"Data for {item['nameOfIssuer']} inserted successfully.")

    print("Data inserted successfully.")

except psycopg2.Error as e:
    print("Error: Unable to connect to the database or insert data.")
    print(e)
