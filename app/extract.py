import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlencode


def extract_jumia_data(base_url, params, headers, MAX_PAGES):
    session = requests.Session()
    session.headers.update(headers)

    shoe_list = []
    

    # IMPORTANT: warm up session (sets cookies like a real browser)
    session.get("https://www.jumia.com.ng/mens-shoes/")

    # =========================
    # 3. SCRAPING LOOP
    # =========================
    while params["page"] <= MAX_PAGES:
        print(f"\nScraping page {params['page']} of {MAX_PAGES}...")

        try:
            full_url = f"{base_url}?{urlencode(params)}"
            print(f"Requesting: {full_url}")
            response = session.get(base_url, params=params, timeout=20)

            print("Status:", response.status_code)
            print("Length:", len(response.text))

            if response.status_code != 200:
                print("Stopped: bad status code")
                break

            # Debug (VERY important for learning)
            print("Sample HTML:", response.text[:300])

            soup = BeautifulSoup(response.text, "html.parser")

            shoes = soup.find_all("a", class_="core")

            print(f"Found {len(shoes)} items on page {params['page']}")

            if not shoes:
                print("No products found. Stopping.")
                break

            # =========================
            # 4. PARSING
            # =========================
            for shoe in shoes:
                try:
                    name_tag = shoe.find("h3", class_="name")
                    price_tag = shoe.find("div", class_="prc")
                    discount = shoe.find("div", class_="bdg _dsct _sm")
                    if not discount:
                        discount = None
                    else:
                        discount = discount.text

                    if not name_tag or not price_tag:
                        continue

                    name = name_tag.text
                    raw_price = price_tag.text

                    link = "https://www.jumia.com.ng" + shoe.get("href", "")

                    shoe_list.append({
                        "Product_name": name,
                        "Price": raw_price,
                        "Link": link,
                        "Discount": discount
                    })

                except Exception as e:
                    print("Parsing error:", e)
                    continue
                

            # next page
            params["page"] += 1
            time.sleep(2)

        except requests.exceptions.RequestException as e:
            print("Connection error:", e)
            time.sleep(10)
            continue
    return shoe_list
