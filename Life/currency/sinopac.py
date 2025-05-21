from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
from config import TARGET_CURRENCIES


def get_sinopac_rates():
    rates = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://bank.sinopac.com/MMA8/bank/html/rate/bank_ExchangeRate.html")
        page.wait_for_timeout(2000)  # Let JS render content
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("table.data-table1 tr")
    print(f"永豐 🔍 Found {len(rows)} raw currency rows to parse.")

    for row in rows:
        tds = row.find_all("td")
        if len(tds) < 3:
            continue

        currency_text = tds[0].get_text(strip=True)
        match = re.search(r"\((\w{3})\)", currency_text)
        if not match:
            continue
        code = match.group(1)
        if code not in TARGET_CURRENCIES:
            continue

        buy_text = tds[1].get_text(strip=True)
        sell_text = tds[2].get_text(strip=True)

        if not buy_text or not sell_text or "-" in (buy_text, sell_text):
            print(f"⚠️ Skipping {code} due to invalid rate.")
            continue

        try:
            bank_buy = float(buy_text)
            bank_sell = float(sell_text)
            print(f"💱 {code} - Buy: {bank_buy}, Sell: {bank_sell}")
            rates[code] = {
                "bank_buy": bank_buy,
                "bank_sell": bank_sell,
                "bank": "永豐"
            }
        except Exception as e:
            print(f"❌ Parse error for {code}: {e}")
            continue

    return rates
