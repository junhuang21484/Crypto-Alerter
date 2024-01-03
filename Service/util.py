from API.birdeye_api import BirdEyeApi


class Util:
    def __init__(self):
        self.birdeye_api = BirdEyeApi("ee766d1fb16f4d3cb46e12a18fb15803")
        self.chain_address_dict = {
            "solana": "So11111111111111111111111111111111111111111"
        }

    def calculate_profit(self, chain: str, wallet_addy: str, token_addy: str, amount_bought: float) -> float:
        user_port = self.birdeye_api.get_wallet_portfolio(chain, wallet_addy)
        bought_value = 0
        token_value = 0

        for token in user_port['items']:
            if token['address'] == token_addy:
                token_value = token['valueUsd']

            if token['address'] == self.chain_address_dict[chain]:
                bought_value = token['priceUsd'] * amount_bought

            if bought_value != 0 and token_value != 0:
                break

        if token_value == 0 or bought_value == 0:
            return -1

        pnl = (token_value - bought_value) / bought_value

        return pnl * 100


