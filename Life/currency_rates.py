
import os
from datetime import datetime
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import pytz

load_dotenv(override=True)
NOTION_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

TARGET_CURRENCIES = ["USD", "AUD", "GBP", "EUR"]

headers = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}


def get_cathay_rates():
    url = "https://www.cathaybk.com.tw/cathaybk/personal/product/deposit/currency-billboard/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    rates = {}

    currency_blocks = soup.select('[select-id]')
    print(f"國泰 🔍 Found {len(currency_blocks)} currency blocks to parse.")

    for block in currency_blocks:
        name_tag = block.select_one(".cubre-m-currency__name")
        if not name_tag:
            continue

        full_currency_name = name_tag.text.strip()
        currency_code = full_currency_name[-3:]

        if currency_code not in TARGET_CURRENCIES:
            continue

        rate_table = block.select_one(".cubre-o-rateCard__content table")
        if not rate_table:
            continue

        tds = rate_table.select("tbody tr:nth-of-type(2) td")
        if len(tds) >= 3:
            try:
                bank_buy = float(tds[1].text.strip().replace(",", ""))
                bank_sell = float(tds[2].text.strip().replace(",", ""))
                rates[currency_code] = {
                    "bank_buy": bank_buy,
                    "bank_sell": bank_sell,
                    "bank": "國泰"

                }
                print(f"💱 {currency_code} - Buy: {bank_buy}, Sell: {bank_sell}")
            except ValueError:
                print(f"⚠️ Could not parse rate for {currency_code}")

    return rates


def get_esun_rates():


    url = "https://www.esunbank.com/zh-tw/personal/deposit/rate/forex/foreign-exchange-rates"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    rows = [r for r in soup.select("tbody tr")[1:] if r.get("class")]

    print(f"玉山 🔍 Found {len(rows)} raw currency rows to parse.")

    rates = {}
    target_currencies = ["USD", "AUD", "GBP", "EUR"]
    rows = [r for r in soup.select("tbody tr")[1:] if r.get("class")]
    valid_count = 0

    for row in rows:
        row_classes = row.get("class", [])

        matched_code = next(
            (code for code in target_currencies if code in row_classes), None)
        if not matched_code:
            continue

        tds = row.find_all("td", recursive=False)
        if len(tds) < 4:
            continue

        rate_td = tds[2]

        try:
            buy_div = rate_td.select_one(".BuyIncreaseRate")
            sell_div = rate_td.select_one(".SellDecreaseRate")

            if not (buy_div and sell_div):
                print(f"⚠️ Missing Buy/Sell divs for {matched_code}")
                continue

            bank_buy = float(buy_div.text.strip())
            bank_sell = float(sell_div.text.strip())

            print(f"💱 {matched_code} - Buy: {bank_buy}, Sell: {bank_sell}")

            rates[matched_code] = {
                "bank_buy": bank_buy,
                "bank_sell": bank_sell,
                "bank": "玉山"
            }
            valid_count += 1

        except Exception as e:
            print(f"❌ Error parsing {matched_code}: {e}")

    return rates


def update_notion_currency(currency, bank_buy, bank_sell, bank):
    search_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(search_url, headers=headers, json={
        "filter": {
            "and": [
                {
                    "property": "Currency",
                    "rich_text": {
                        "equals": currency
                    }
                },
                {
                    "property": "Bank",
                    "select": {
                        "equals": bank
                    }
                }
            ]
        }

    })

    data = response.json()
    if response.status_code != 200:
        print(f"❌ Error querying Notion for {currency}: {data}")
        return

    if not data.get("results"):
        print(f"⚠️ Currency {currency} not found in Notion database.")
        return

    page_id = data["results"][0]["id"]
    update_url = f"https://api.notion.com/v1/pages/{page_id}"

    tz = pytz.timezone("Asia/Taipei")
    now_iso = datetime.now(tz).isoformat()

    payload = {
        "properties": {
            "Bank": {"select": {"name": bank}},
            "Bank Buy": {"number": bank_buy},
            "Bank Sell": {"number": bank_sell},
            "Last Updated": {"date": {"start": now_iso}}
        }
    }

    update_res = requests.patch(update_url, headers=headers, json=payload)
    if update_res.status_code == 200:
        print(f"✅ {currency} updated successfully in Notion.")
    else:
        print(f"❌ Failed to update {currency}: {update_res.json()}")


if __name__ == "__main__":
    print("🚀 Starting currency rate updater...")

    cathay_rates = get_cathay_rates()
    esun_rates = get_esun_rates()

    rates = {**cathay_rates, **esun_rates}

    if not rates:
        print("⚠️ No rates were scraped. Check the site or scraping logic.")
    else:
        for currency, values in rates.items():
            update_notion_currency(
                currency, values["bank_sell"], values["bank_buy"], values["bank"])

    print("✅ Exchange rates updated to Notion.")
