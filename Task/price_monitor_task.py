from API.birdeye_api import BirdEyeApi
from API.discord_api import DiscordAPI

import threading
import time


class PriceMonitorTask:
    def __init__(self, chain: str, token: str, alert_condition: list, check_interval: int, alert_interval: int, birdeye_api: BirdEyeApi,
                 discord_api: DiscordAPI):
        self.chain = chain
        self.token = token
        self.alert_condition = alert_condition
        self.check_interval = check_interval
        self.alert_interval = alert_interval
        self.birdeye_api = birdeye_api
        self.discord_api = discord_api

        self.token_price = 0

    def check_token_price(self, stop_event: threading.Event):
        while not stop_event.is_set():
            self.token_price = self.birdeye_api.get_crypto_price(self.chain, self.token)
            time.sleep(self.check_interval)

    def check_conditions(self):
        for condition in self.alert_condition:
            if condition['type'] == 'above' and self.token_price > condition['amt']:
                return condition

            if condition['type'] == 'below' and self.token_price < condition['amt']:
                return condition

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
                pass


