import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
import psycopg2
from decouple import config

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host=config('POSTGRES_HOST'),
    port="5432",
    database="value_stocks_Q423",
    user=config('POSTGRES_USER'),
    password=config('POSTGRES_PASSWORD')
)

cur = conn.cursor()

# Check if the table exists, and create it if it doesn't

create_table_query = f'''
    CREATE TABLE IF NOT EXISTS public.value_stocks (
        tickers VARCHAR(10),
        trailingPE NUMERIC,
        longName VARCHAR(100),
        priceToSalesTrailing12Months NUMERIC,
        trailingEps NUMERIC,
        forwardPE NUMERIC,
        marketCap NUMERIC,
        grossMargins NUMERIC,
        returnOnAssets NUMERIC,
        returnOnEquity NUMERIC
    );
    '''
cur.execute(create_table_query)
conn.commit()

# Send an HTTP GET request to the URL
url = "https://www.morningstar.com/stocks/33-undervalued-stocks-2"
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the elements containing the ticker symbols
    ticker_elements = soup.find_all(
        "a", class_="mdc-link mds-link mdc-link--body")

    # Extract the tickers from the elements
    tickers = [element.get_text()
               for element in ticker_elements if len(element.get_text()) < 5]

    # Create a DataFrame with the tickers
    df = pd.DataFrame({"Tickers": tickers})

    # Define the financial metrics you want to retrieve
    financial_metrics = [
        "trailingPE", "longName", "priceToSalesTrailing12Months",
        "trailingEps", "forwardPE", "marketCap",
        "grossMargins", "returnOnAssets", "returnOnEquity"
    ]

    # Fetch and add the financial metrics to the DataFrame
    for metric in financial_metrics:
        df[metric] = [yf.Ticker(ticker).info.get(metric) for ticker in tickers]


    # Iterate through the tickers and insert data into the table using SQL INSERT
    for ticker in tickers:
        data = yf.Ticker(ticker).info
        insert_query = '''
            INSERT INTO public.value_stocks (tickers, trailingPE, longName,
            priceToSalesTrailing12Months, trailingEps, forwardPE, marketCap,
            grossMargins, returnOnAssets, returnOnEquity)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        insert_data = (
            ticker,
            data.get("trailingPE"),
            data.get("longName"),
            data.get("priceToSalesTrailing12Months"),
            data.get("trailingEps"),
            data.get("forwardPE"),
            data.get("marketCap"),
            data.get("grossMargins"),
            data.get("returnOnAssets"),
            data.get("returnOnEquity")
        )
        cur.execute(insert_query, insert_data)

    conn.commit()

    conn.close()
else:
    print("Failed to retrieve the page. Status code:", response.status_code)
