import time

import requests
import threading


class DexscreenerApi:
    def get_token_info(self, token: str) -> dict:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{token}"
        resp = requests.get(url)
        resp = resp.json()
        print(resp)
        if resp['pairs']:
            d = resp['pairs'][0]
            print(d)
            return {
                "chain": d['chainId'],
                "name": d['baseToken']['name'],
                'symbol': d['baseToken']['symbol']
            }

    def get_token_price(self, token: str) -> float:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{token}"
        resp = requests.get(url)
        resp = resp.json()
        if resp['pairs']:
            return resp['pairs']['priceUsd']

        return -1

    def loop_until_found(self, token: str, check_interval: int, found_event: threading.Event):
        while not found_event.is_set():
            d = self.get_token_info(token)
            if d:
                found_event.set()
            else:
                time.sleep(check_interval)
