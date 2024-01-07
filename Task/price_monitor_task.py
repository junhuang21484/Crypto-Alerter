from API.crypto_info_api import CryptoInfoApi
from API.discord_api import DiscordAPI

import threading
import time
import logging


class PriceMonitorTask:
    def __init__(self, token: str, alert_condition: list, check_interval: int, alert_interval: int,
                 crypto_info_api: CryptoInfoApi, discord_api: DiscordAPI):
        self.token = token
        self.alert_condition = alert_condition
        self.check_interval = check_interval
        self.alert_interval = alert_interval
        self.crypto_info_api = crypto_info_api
        self.discord_api = discord_api

        self.token_price = 0
        self.token_info = self.crypto_info_api.get_token_info(token)

    def check_token_price(self, stop_event: threading.Event):
        while not stop_event.is_set():
            self.token_price = self.crypto_info_api.check_token_price(self.token)
            logging.info(f"Token price update {self.token} ({self.token_price})")
            time.sleep(self.check_interval)

    def check_conditions(self):
        for condition in self.alert_condition:
            condition_type = condition['type']
            condition_price = condition['price']
            if condition_type == 'above' and self.token_price > condition_price:
                return f"Price Above ${condition_price:.15f}"

            if condition_type == 'below' and self.token_price < condition_price:
                return f"Price Below ${condition_price:.15f}"

        return

    def start(self, stop_event: threading.Event):
        price_thread = threading.Thread(target=self.check_token_price, args=(stop_event,))
        price_thread.start()

        old_price = self.token_price
        while not stop_event.is_set():
            if old_price == self.token_price:
                continue

            old_price = self.token_price

            condition_meet = self.check_conditions()
            if condition_meet:
                logging.info(f"Sending alert for token {self.token}")
                embed_data = self.discord_api.create_alert_embed("Pricing", self.token, f"{self.token_price:.15f}",
                                                                 condition_meet)
                msg = f"{self.token} - {self.token_info['chain']}"
                self.discord_api.send_webhook_embed(msg, embed_data)
                time.sleep(self.alert_interval)

        logging.info("Stop event triggered - task has stopped")
