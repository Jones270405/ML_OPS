import pandas as pd
import numpy as np

np.random.seed(42)

rows = 10000
price = 42000

timestamps = pd.date_range(start="2024-01-01", periods=rows, freq="min")

data = []

for ts in timestamps:
    change = np.random.normal(0, 50)
    open_price = price
    close_price = price + change

    high_price = max(open_price, close_price) + np.random.uniform(0, 30)
    low_price = min(open_price, close_price) - np.random.uniform(0, 30)

    volume_btc = np.random.uniform(10, 200)
    volume_usd = volume_btc * close_price

    data.append([
        ts,
        round(open_price, 2),
        round(high_price, 2),
        round(low_price, 2),
        round(close_price, 2),
        round(volume_btc, 2),
        round(volume_usd, 2)
    ])

    price = close_price

df = pd.DataFrame(data, columns=[
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume_btc",
    "volume_usd"
])

df.to_csv("data.csv", index=False)

print("data.csv created with 10,000 rows.")