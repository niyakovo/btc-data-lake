import requests
import time
import csv
import os
from datetime import datetime

def fetch_binance_price():
    while True:
        try:
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            response = requests.get(url)
            data = response.json()

            price = float(data['price'])
            ts = datetime.now()

            filename = f"./data_lake/btc_{ts.strftime('%Y%m%d_%H%M%S')}.csv"

            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['timestamp', 'price'])
                writer.writerow([ts.isoformat(), price])

            print(f"Binance: {price} USDT saved to {filename}")

        except Exception as e:
            print(f"Connection error with Binance: {e}")

    time.sleep(1)

if __name__ == "__main__":
    fetch_binance_price()
