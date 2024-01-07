import logging

from Task.price_monitor_task import PriceMonitorTask
from API.discord_api import DiscordAPI
from API.crypto_info_api import CryptoInfoApi

import json
import threading


class TaskProcessor:
    def __init__(self, check_interval: int, alert_interval: int, crypto_info_api: CryptoInfoApi,
                 discord_api: DiscordAPI):
        self.check_interval = check_interval
        self.alert_interval = alert_interval
        self.crypto_info_api = crypto_info_api
        self.discord_api = discord_api

        self.price_monitor_task_location = "Data/price_monitor_task.json"
        self.price_monitor_task = json.load(open(self.price_monitor_task_location, "r"))
        self.accepted_task_type = ["price", "position"]

        self.running_task = {}

    def show_price_monitor_task(self):
        show_str = "Price Monitor Task\n"
        for i, task in enumerate(self.price_monitor_task['tasks']):
            alert_when = [f'{x["type"]} ${x["price"]:}' for x in task['alert_when']]
            alert_when = '\n'.join(alert_when)
            show_str += f"Task ID: {i} [Price]\n" \
                        f"Chain: {task['token_data']['chain']}\n" \
                        f"Token: {task['token']}\n" \
                        f"Alert When:\n{alert_when}\n" \
                        f"Start command: start_task price {i}\n\n"

        print(show_str)

    def add_task_data(self, task_type, task_data):
        if task_type == "price":
            self.price_monitor_task["tasks"].append(task_data)
            json.dump(self.price_monitor_task, open(self.price_monitor_task_location, "w"), indent=4)

        logging.info("Task added")

    def start_task(self, task_type, data_index):
        data_source = self.price_monitor_task if task_type == "price" else {}

        if data_index >= len(data_source['tasks']):
            logging.info("Task start failed - task index out of range")
            return

        task_data = data_source["tasks"][data_index]
        task_key = f"{task_type}-{len(self.running_task)}"

        task = PriceMonitorTask(task_data['token'], task_data['alert_when'], self.check_interval, self.alert_interval,
                                self.crypto_info_api, self.discord_api)

        task_stop_event = threading.Event()
        task_thread = threading.Thread(target=task.start, args=(task_stop_event,))
        task_thread.start()

        self.running_task[task_key] = {
            "type": task_type,
            "token": task_data['token'],
            "thread_instance": task_thread,
            "stop_event": task_stop_event
        }

        logging.info(f"Task started running for token {task_data['token_data']['chain']}-{task_data['token']}")

    def stop_task(self, task_type, task_index):
        key = f"{task_type}-{task_index}"
        if key not in self.running_task:
            logging.info(f"Stop task failed, cannot locate {task_type}-{task_index}")
            return

        task_data = self.running_task[key]
        task_data['stop_event'].set()
        logging.info(f"Task {key} will stop shortly")
