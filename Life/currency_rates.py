
import os
from datetime import datetime
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import pytz

load_dotenv(override=True)
NOTION_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}


def get_currency_rates():
    url = "https://www.cathaybk.com.tw/cathaybk/personal/product/deposit/currency-billboard/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    rates = {}
    target_currencies = ["USD", "AUD", "GBP", "EUR"]

    currency_blocks = soup.select('[select-id]')
    print(f"🔍 Found {len(currency_blocks)} currency blocks to parse.")

    for block in currency_blocks:
        name_tag = block.select_one(".cubre-m-currency__name")
        if not name_tag:
            continue

        full_currency_name = name_tag.text.strip()
        currency_code = full_currency_name[-3:]

        if currency_code not in target_currencies:
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
                    "bank_sell": bank_sell
                }
                print(f"💱 {currency_code} - Buy: {bank_buy}, Sell: {bank_sell}")
            except ValueError:
                print(f"⚠️ Could not parse rate for {currency_code}")

    return rates


def update_notion_currency(currency, bank_buy, bank_sell):
    search_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(search_url, headers=headers, json={
        "filter": {
            "property": "Currency",
            "rich_text": {
                "equals": currency
            }
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


def test_notion_connection():
    print("🔐 Testing Notion API token and database ID...")
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"

    print("🔗 URL:", url)
    print("🔑 Token:", NOTION_KEY)

    res = requests.get(url, headers=headers)
    print(f"📡 Status code: {res.status_code}")
    try:
        data = res.json()
    except Exception:
        print("⚠️ Could not decode response as JSON")
        print(res.text)
        return

    if res.status_code == 200:
        print("✅ Success! Token and DB access confirmed.")
        print("📄 Database title:", data['title'][0]['plain_text'])
    else:
        print("❌ Failed. Details:")
        print(data)


if __name__ == "__main__":
    print("🚀 Starting currency rate updater...")
    rates = get_currency_rates()
    if not rates:
        print("⚠️ No rates were scraped. Check the site or scraping logic.")
    else:
        for currency, values in rates.items():
            update_notion_currency(
                currency, values["bank_sell"], values["bank_buy"])

    print("✅ Exchange rates updated to Notion.")
