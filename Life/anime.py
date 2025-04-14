import requests
from bs4 import BeautifulSoup
import json
from discord_webhook import DiscordWebhook

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1361387010174091288/YI-RlZWDJrcHhL3lbrhtl0k7GoZIm8dXzz8YUMVAr3l4m2tymdaonbAtxUvjGFcMOmFU'

TRACKED_SERIES = {
    "藥師少女的獨語 第二季": "https://anime1.me/category/2025年冬季/藥師少女的獨語-第二季",
    "不會拿捏距離的阿波連同學 第二季": "https://anime1.me/category/2025年冬季/不會拿捏距離的阿波連同學-第二季"
}

STATE_FILE = 'anime_tracker_state.json'


def load_state():
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=4)


def fetch_latest_episode(series_url):
    print(f"Fetching series page: {series_url}")
    response = requests.get(series_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    titles = soup.select('.entry-title a')
    print(f"🔍 Found {len(titles)} post(s) with '.entry-title a'")
    for t in titles:
        print(f" - {t.get_text(strip=True)}")

    # Correct selector for category pages
    post = soup.select_one('.entry-title a')
    if post:
        title = post.get_text(strip=True)
        link = post['href']
        print(f"✅ Found latest post: {title}")
        return {'title': title, 'url': link}
    else:
        print("⚠️  No post found on page.")
        return None


def send_discord_notification(series, episode_info):
    content = f"🎉 New episode for **{series}**!\n{episode_info['title']}\n{episode_info['url']}"
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=content)
    response = webhook.execute()
    if response.status_code == 200:
        print(f"✅ Notification sent for {series}: {episode_info['title']}")
    else:
        print(
            f"❌ Failed to send notification for {series}: {response.status_code}")


def main():
    state = load_state()

    for series, url in TRACKED_SERIES.items():
        print(f"Processing series: {series}")
        latest_episode = fetch_latest_episode(url)

        if not latest_episode:
            continue

        last_notified = state.get(series)
        print(f"Last notified for {series}: {last_notified}")

        if not last_notified or latest_episode['title'] != last_notified:
            send_discord_notification(series, latest_episode)
            state[series] = latest_episode['title']

    save_state(state)
    print("✅ State saved.")


if __name__ == "__main__":
    main()
