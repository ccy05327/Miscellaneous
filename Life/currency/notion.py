from config import DATABASE_ID, headers
import requests
from datetime import datetime
import pytz
import os

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
            "Bank Buy (I Sell)": {"number": bank_buy},
            "Bank Sell (I Buy)": {"number": bank_sell},
            "Last Updated": {"date": {"start": now_iso}}
        }
    }

    update_res = requests.patch(update_url, headers=headers, json=payload)
    if update_res.status_code == 200:
        pass
    else:
        print(f"❌ Failed to update {currency}: {update_res.json()}")


def fetch_owned_currency_data():
    headers = {
        "Authorization": f"Bearer {os.getenv('NOTION_API_KEY')}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    query_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    payload = {
        "filter": {
            "or": [
                {
                    "property": "Status",
                    "select": {
                        "equals": "Owned"
                    }
                },
                {
                    "property": "Status",
                    "select": {
                        "equals": "Watching"
                    }
                }
            ]
        }
    }

    try:
        res = requests.post(query_url, headers=headers,
                            json=payload, timeout=10)
        res.raise_for_status()
        results = res.json().get("results", [])
        print(f"🔍 Found {len(results)} currency rows to parse.")
    except requests.exceptions.Timeout:
        print("❌ Notion API timed out.")
    except requests.exceptions.HTTPError as err:
        print(
            f"❌ HTTP error from Notion: {err.response.status_code} - {err.response.text}")

    currency_data = []

    for page in results:
        if not page.get("properties"):
            print("⚠️ No properties found in page.")
            continue

        props = page["properties"]

        try:
            currency_data.append({
                "currency": props.get("Currency", {}).get("title", [{}])[0].get("plain_text", "Unknown"),
                "bank": props.get("Bank", {}).get("select", {}).get("name", "Unknown"),
                "bank_sell": props.get("Bank Sell (I Buy)", {}).get("number"),
                "bank_buy": props.get("Bank Buy (I Sell)", {}).get("number"),
                "holding": props.get("Holding", {}).get("number"),
                "weighted_rate": props.get("weighted rate", {}).get("number"),
                "current_value": props.get("Current Value", {}).get("formula", {}).get("number"),
                "profit": props.get("Profit", {}).get("formula", {}).get("number"),
                "return_pct": props.get("Return %", {}).get("formula", {}).get("number"),
                "status": props.get("Status", {}).get("select", {}).get("name", "Unknown"),
                "notion_url": page.get("url")
            })

        except Exception as e:
            print(f"⚠️ Failed to parse one row: {e}")

    return currency_data
