from API.crypto_info_api import CryptoInfoApi
from Service.task_processor import TaskProcessor


class CommandProcessor:
    def __init__(self, crypto_info_api: CryptoInfoApi, task_processor: TaskProcessor):
        self.accepted_commands = {
            "create_task": self.cmd_create_task,
            "start_task": self.cmd_start_task,
            "stop_task": self.cmd_stop_task,
            "show_task": self.cmd_show_task
        }
        self.crypto_info_api = crypto_info_api
        self.task_processor = task_processor

    def cmd_create_task(self, cmd_data):
        if cmd_data[0] not in self.task_processor.accepted_task_type:
            print(
                f"TASK CREATION FAILED - Cannot create a {cmd_data[0]} task, only {'|'.join(self.task_processor.accepted_task_type)} task accepted")
            return

        if len(cmd_data) != 3:
            print("TASK CREATION FAILED - Invalid argument format")
            return

        token = cmd_data[1]
        if not self.crypto_info_api.check_token_exist(token):
            print("Invalid token provided")
            return

        alert_list = cmd_data[2].split(',')
        alert_when = [{"type": d.split("-")[0], "price": float(d.split("-")[1])} for d in alert_list]

        token_data = self.crypto_info_api.get_token_info(token)
        task_data = {
            "token": token, "token_data": token_data, "alert_when": alert_when
        }
        self.task_processor.add_task_data(cmd_data[0], task_data)

    def cmd_show_task(self, cmd_data):
        self.task_processor.show_price_monitor_task()

    def cmd_start_task(self, cmd_data):
        if len(cmd_data) != 2:
            print("TASK START FAILED - Invalid argument format")
            return

        if cmd_data[0] not in self.task_processor.accepted_task_type:
            print(
                f"TASK START FAILED - Cannot start a {cmd_data[0]} task, only {'|'.join(self.task_processor.accepted_task_type)} task accepted")
            return

        self.task_processor.start_task(cmd_data[0], int(cmd_data[1]))

    def cmd_stop_task(self, cmd_data):
        # Implementation for 'stop' command
        if len(cmd_data) != 2:
            print("TASK START FAILED - Invalid argument format")
            return

        if cmd_data[0] not in self.task_processor.accepted_task_type:
            print(
                f"TASK START FAILED - Cannot start a {cmd_data[0]} task, only {'|'.join(self.task_processor.accepted_task_type)} task accepted")
            return

        self.task_processor.stop_task(cmd_data[0], int(cmd_data[1]))

    def handle_cmd(self):

        while True:
            cmd_str = input("")
            cmd_data = cmd_str.split(" ")
            command_name = cmd_data[0]

            if command_name not in self.accepted_commands:
                print(f"Command {command_name} not accepted")
                continue

            if len(cmd_data) == 1:
                cmd_data.append("")

            self.accepted_commands[command_name](cmd_data[1:])
