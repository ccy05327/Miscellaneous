from config import TARGET_CURRENCIES


def get_cathay_rates():
    import requests
    from bs4 import BeautifulSoup

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
