import requests


class DiscordAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://discord.com/api/v10"

    def send_webhook_embed(self, webhook: str, msg: str, embed_data: list[dict]) -> bool:
        url = webhook

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        data = {"content": msg, "embeds": embed_data}
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 204:
            return True

        return False


wh = "https://discord.com/api/webhooks/1190886769948901526/NW0dfD2LqZI2ARFVudyUWYn0-LIvEXdgm41Okv1Oo_TudWvErAHoY2MnJ0AL-gWyP9wo"
da = [
    {
        "title": "Pricing Alert Triggered",
        "color": 0xb81855,
        "fields": [
            {
                "name": "Token",
                "value": "9gwTegFJJErDpWJKjPfLr2g2zrE3nL1v5zpwbtsk3c6P",
                "inline": False
            },
            {
                "name": "Alert Reason",
                "value": "Price dropped 20%",
                "inline": True
            },
            {
                "name": "Current Price",
                "value": "$0.9123",
                "inline": True
            },
            {
                "name": "PnL",
                "value": "20%",
                "inline": True
            }
        ]
    }
]

d = DiscordAPI('a')
d.send_webhook_embed(wh, "USED HONDA - SOL", da)
