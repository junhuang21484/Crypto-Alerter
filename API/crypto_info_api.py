import threading

from API.birdeye_api import BirdEyeApi
from API.dexscreener_api import DexscreenerApi

import json


class CryptoInfoApi:
    def __init__(self, birdeye_api: BirdEyeApi, dexscreener_api: DexscreenerApi):
        self.birdeye_api = birdeye_api
        self.dexscreener_api = dexscreener_api

        self.token_data = json.load(open("Data/token_info.json", "r"))

    def update_token_data(self, token: str, data: dict):
        self.token_data[token] = data
        json.dump(self.token_data, open("Data/token_info.json", 'w'), indent=4)

    def check_token_exist(self, token: str) -> bool:
        if token in self.token_data:
            return True
        else:
            data = self.dexscreener_api.get_token_info(token)
            self.update_token_data(token, data)
            if data:
                return True

        return False

    def check_token_price(self, token: str) -> float:
        chain = self.token_data[token]['chain']
        if self.birdeye_api.check_chain_supported(chain):
            price = self.birdeye_api.get_crypto_price(chain, token)
        else:
            price = self.dexscreener_api.get_token_price(token)

        return price

    def get_token_info(self, token: str):
        return self.token_data[token] if token in self.token_data else None

    def wait_till_token_live(self, chain: str, token: str, check_interval: int):
        found_event = threading.Event()
