from dotenv import load_dotenv
from esun import get_esun_rates
from sinopac import get_sinopac_rates
from cathay import get_cathay_rates
from notion import update_notion_currency, fetch_owned_currency_data
from send_email import send_summary_email
from pathlib import Path
import os

# Get the full path to .env relative to the script location
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path="D:/GitHub/Miscellaneous/Life/.env", override=True)

print("✅ NOTION_API_KEY loaded:", os.getenv("NOTION_API_KEY") is not None)


def main():
    print("🚀 Starting currency rate updater...")

    # --- Get rates from all banks ---
    cathay_rates = get_cathay_rates()
    esun_rates = get_esun_rates()
    sinopac_rates = get_sinopac_rates()

    # --- Combine all into one dict ---
    combined = {}

    for currency, values in cathay_rates.items():
        combined[(currency, values["bank"])] = values

    for currency, values in esun_rates.items():
        combined[(currency, values["bank"])] = values

    for currency, values in sinopac_rates.items():
        combined[(currency, values["bank"])] = values

    # --- Update Notion ---
    if not combined:
        print("⚠️ No rates were scraped. Check the site or scraping logic.")
    else:
        for (currency, bank), values in combined.items():
            print(f"💾 Updating {currency} ({bank}) to Notion...")
            update_notion_currency(
                currency,
                values["bank_sell"],
                values["bank_buy"],
                bank
            )

    print("✅ Exchange rates updated to Notion.")

    currency_data = fetch_owned_currency_data()
    send_summary_email(currency_data)


if __name__ == "__main__":
    main()
