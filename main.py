from API.birdeye_api import BirdEyeApi
from API.dexscreener_api import DexscreenerApi
from API.crypto_info_api import CryptoInfoApi
from API.discord_api import DiscordAPI
from Service.task_processor import TaskProcessor
from Service.command_processor import CommandProcessor

import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)s] %(levelname)s: %(message)s"
)


def main():
    logging.info("Initializing The System")

    setting = json.load(open("Data/setting.json", "r"))
    birdeye_api = BirdEyeApi(setting['birdeye']['api_key'])
    dexscreener_api = DexscreenerApi()
    crypto_info_api = CryptoInfoApi(birdeye_api, dexscreener_api)
    discord_api = DiscordAPI(setting['alert']['discord']['webhook'])
    task_processor = TaskProcessor(setting['price_monitor']['check_interval'], setting['price_monitor']['alert_interval'], crypto_info_api, discord_api)
    cmd_processor = CommandProcessor(crypto_info_api, task_processor)
    logging.info("System started, starting to accept commands")
    cmd_processor.handle_cmd()


if __name__ == '__main__':
    main()
