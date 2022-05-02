from wsgiref import headers
import requests

LINE_TO_ME_TOKEN = 'HisNFhyDkaIvg9yfoBn3ZMMlCNKdqRknv506RnPxo0c'
# might have other tokens for other LINE groups
URL = "https://notify-api.line.me/api/notify"

headers = {
    "Authorization": "Bearer " + LINE_TO_ME_TOKEN,
    "Content-Type": "application/x-www-form-urlencoded"
}
payload = {'message': "some test texts"}
notify = requests.post(URL, headers=headers, params=payload)
if notify.status_code == 200:
    print("Message sent!")
else:
    print("Failed...")
