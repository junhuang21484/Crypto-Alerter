import requests
import threading
import time


class BirdEyeApi:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://public-api.birdeye.so"

        self.supported_chain = self.get_supported_chain()

    def get_supported_chain(self) -> list[str]:
        url = self.base_url + "/v1/wallet/list_supported_chain"
        headers = {"X-API-KEY": self.api_key}

        response = requests.get(url, headers=headers).json()
        if response['success']:
            return response['data']

        return ["solana", "ethereum", "arbitrum", "avalanche", "bsc", "optimism", "polygon", "base",
                "zksync"]

    def get_crypto_price(self, chain: str, token_addy: str) -> float:
        url = self.base_url + f"/public/price?address={token_addy}"

        headers = {
            "x-chain": chain,
            "X-API-KEY": self.api_key
        }

        response = requests.get(url, headers=headers).json()
        if response['success'] and response['data']:
            return response['data']['value']
        elif not response['success']:
            print(response)

        return -1

    def get_wallet_portfolio(self, chain: str, wallet_addy: str) -> []:
        url = self.base_url + f"/v1/wallet/token_list?wallet={wallet_addy}"

        headers = {
            "x-chain": chain,
            "X-API-KEY": self.api_key
        }
        response = requests.get(url, headers=headers).json()
        if response['success']:
            return response['data']

        return []

    def check_chain_supported(self, chain: str) -> bool:
        return chain in self.supported_chain

    def loop_until_found(self, chain: str, token: str, check_interval: int, found_event: threading.Event):
        while not found_event.is_set():
            d = self.get_crypto_price(chain, token)
            if d:
                found_event.set()
            else:
                time.sleep(check_interval)
