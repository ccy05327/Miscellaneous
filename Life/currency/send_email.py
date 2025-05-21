from email.message import EmailMessage
import smtplib
import os


def send_summary_email(scraped_data):
    from_email = "explorationyear2020@gmail.com"
    to_email = "ccy05327@duck.com"
    subject = "📊 Currency Tracker Update"
    if not scraped_data:
        print("⚠️ No data to send.")
        return

    owned = [d for d in scraped_data if d.get("status") == "Owned"]
    watching = [d for d in scraped_data if d.get("status") == "Watching"]

    print(
        f"🔍 Found {len(owned)} owned and {len(watching)} watching currencies.")

    owned_cards = ""
    for data in owned:
        color = get_color(data.get("return_pct"))
        owned_cards += f"""
        <table style="background-color:#fff; border-collapse:collapse; width:100%; max-width:500px; margin-bottom:25px; box-shadow:0 2px 6px rgba(0,0,0,0.08);">
            <tr><td style="font-weight:bold; background:#f4f6fa; padding:10px;">銀行 / 幣別</td><td style="padding:10px;">{data['bank']} / {data['currency']}</td></tr>
            <tr><td style="font-weight:bold; background:#f4f6fa; padding:10px;">目前賣出 (I buy)</td><td style="padding:10px;">{data['bank_sell']}</td></tr>
            <tr><td style="font-weight:bold; background:#f4f6fa; padding:10px;">目前買入 (I sell)</td><td style="padding:10px;">{data['bank_buy']}</td></tr>
            <tr><td style="font-weight:bold; background:#f4f6fa; padding:10px;">持有數量</td><td style="padding:10px;">{data['holding']}</td></tr>
            <tr><td style="font-weight:bold; background:#f4f6fa; padding:10px;">加權平均成本</td><td style="padding:10px;">{data['weighted_rate']}</td></tr>
            <tr><td style="font-weight:bold; background:#f4f6fa; padding:10px;">現有價值</td><td style="padding:10px;">NTD {data['current_value']}</td></tr>
            <tr><td style="font-weight:bold; background:#f4f6fa; padding:10px;">目前 Profit</td><td style="padding:10px;">NTD {data['profit']}</td></tr>
            <tr><td style="font-weight:bold; background:#f4f6fa; padding:10px;">投報率</td><td style="padding:10px; color:{color}; font-weight:bold;">{round(data['return_pct'] * 100, 2)}%</td></tr>
            <tr><td colspan="2" style="padding:10px;"><a href="{data.get('notion_url', '#')}" style="color:#2e86de;">🔗 點我查看 Notion 頁面</a></td></tr>
        </table>
        """

    watching_cards = ""
    for d in watching:
        watching_cards += f"""
        <table style="border-collapse: collapse; background-color: #ffffff; width: 100%; max-width: 500px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <tr>
                <td style="font-weight: bold; padding: 10px 12px; background-color: #f8f9fa;">幣別 / 銀行</td>
                <td style="padding: 10px 12px;">{d['currency']} / {d['bank']}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; padding: 10px 12px; background-color: #f8f9fa;">目前賣出 (I buy)</td>
                <td style="padding: 10px 12px;">{d['bank_sell']}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; padding: 10px 12px; background-color: #f8f9fa;">目前買入 (I sell)</td>
                <td style="padding: 10px 12px;">{d['bank_buy']}</td>
            </tr>
        </table>
        """

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f7f9fa; padding: 20px;">
        <h2 style="color: #2e86de;">📊 持有幣別</h2>
        {owned_cards or "<p>目前沒有持有資料。</p>"}

        <h2 style="color: #2e86de; margin-top: 30px;">👀 關注幣別</h2>
        {watching_cards or "<p>目前沒有觀察資料。</p>"}

        <p style="font-size: 13px; color: #999999; margin-top: 20px;">This is an automated update from your tracker 📬</p>
    </body>
    </html>
    """

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content("Your email client doesn't support HTML.")
    msg.add_alternative(html, subtype='html')

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(from_email, os.getenv("EMAIL_APP_PASSWORD"))
            smtp.send_message(msg)
            print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Email failed: {e}")


def get_color(return_pct):
    if return_pct > 0:
        return "#27ae60"
    elif return_pct < 0:
        return "#c0392b"
    return "#7f8c8d"
