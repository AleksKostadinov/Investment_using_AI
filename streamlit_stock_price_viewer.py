import streamlit as st
import pandas as pd
import yfinance as yf

st.title("Stock Price Viewer")

stock_symbols = ['NVDA', 'AMD', 'INTC']

stock_data_dict = {}

for symbol in stock_symbols:
    stock_data = yf.Ticker(symbol)
    stocks_df = stock_data.history(period='1y', start='2018-10-13', end='2023-10-13')
    stock_data_dict[symbol] = stocks_df

# Combine the closing prices of all stocks into a single DataFrame
combined_data = pd.DataFrame()
for symbol, data in stock_data_dict.items():
    combined_data[symbol] = data['Close']
    combined_data = combined_data.div(combined_data.iloc[0]).mul(1)

# Display a line chart with all the closing prices
st.subheader("Combined Stock Prices")
st.line_chart(combined_data)

# streamlit run streamlit_stock_price_viewer.py
