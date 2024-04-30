import yfinance as yf

msft = yf.Ticker("MSFT")
if msft.history(period="1d").empty:
    print("No data")
else:
    print("Data available")
