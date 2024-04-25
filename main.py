# -*- coding: utf-8 -*-

import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.binance.com/en/markets/overview"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/58.0.3029.110 Safari/537.3"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

crypto_data = []

for page in range(1, 12):

    names = soup.find_all("div", class_="css-cn2h2t")
    prices = soup.find_all("div", class_="body2 items-center css-18yakpx")
    changes = soup.find_all("div", class_="subtitle3 css-18jvuxg")
    one_day_volumes = soup.find_all("div", class_="body2 text-t-primary css-18yakpx")

    page_data = [{"name": names[i].text,
                  "price": prices[i].text,
                  "change": changes[i].text,
                  "24h_volume": one_day_volumes[i].text}

                 for i in range(min(len(names), len(prices), len(changes), len(one_day_volumes)))]

    crypto_data.append(pd.DataFrame(page_data))

crypto_df = pd.concat(crypto_data, ignore_index=True)

crypto_df.to_csv('crypto_info.csv', index=False, encoding="utf-8", sep=";")
