import pandas as pd
import yfinance as yf
import requests

EXCHANGE_API = "https://api.exchangerate.host/latest?base={}"

def get_exchange_rate(currency):
    if currency == "GBP":
        return 1
    response = requests.get(EXCHANGE_API.format(currency))
    data = response.json()
    return data["rates"]["GBP"]

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    price = stock.history(period="1d")["Close"].iloc[0]
    return price

def calculate_portfolio_value():
    df = pd.read_csv("portfolio.csv")
    total_value_gbp = 0

    for _, row in df.iterrows():
        price = get_stock_price(row["ticker"])
        value_local = price * row["quantity"]
        rate = get_exchange_rate(row["currency"])
        value_gbp = value_local * rate
        total_value_gbp += value_gbp

        print(
            f"{row['ticker']} value in GBP: {value_gbp:.2f}"
        )

    print(f"\nTotal portfolio value in GBP: {total_value_gbp:.2f}")

if __name__ == "__main__":
    calculate_portfolio_value()
