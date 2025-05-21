from config import TARGET_CURRENCIES


def get_esun_rates():
    import requests
    from bs4 import BeautifulSoup

    url = "https://www.esunbank.com/zh-tw/personal/deposit/rate/forex/foreign-exchange-rates"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    rows = [r for r in soup.select("tbody tr")[1:] if r.get("class")]

    print(f"玉山 🔍 Found {len(rows)} raw currency rows to parse.")

    rates = {}
    rows = [r for r in soup.select("tbody tr")[1:] if r.get("class")]
    valid_count = 0

    for row in rows:
        row_classes = row.get("class", [])

        matched_code = next(
            (code for code in TARGET_CURRENCIES if code in row_classes), None)
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
