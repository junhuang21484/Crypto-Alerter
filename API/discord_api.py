import requests


class DiscordAPI:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

        self.base_url = "https://discord.com/api/v10"

    def send_webhook_embed(self, msg: str, embed_data: list[dict]) -> bool:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        data = {"content": msg, "embeds": embed_data}
        response = requests.post(self.webhook_url, headers=headers, json=data)

        if response.status_code == 204:
            return True

        return False

    def create_alert_embed(self, alert_type, token_addy, token_price, alert_reason):
        embed_data = [
            {
                "title": f"{alert_type} Alert Triggered",
                "color": 0xb81855,
                "fields": [
                    {"name": "Token", "value": token_addy, "inline": False},
                    {"name": "Current Token Price", "value": f"${token_price}", "inline": True},
                    {"name": "", "value": f"", "inline": True},
                    {"name": "Alert Reason", "value": alert_reason, "inline": True}
                ]
            }
        ]

        return embed_data

