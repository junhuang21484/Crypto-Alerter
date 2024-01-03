import json


class CommandProcessor:
    def __init__(self):
        self.accepted_commands = {
            "create": self.cmd_create,
            "start": self.cmd_start,
            "stop": self.cmd_stop
        }
        self.price_monitor_task = json.load(open("../Data/price_monitor_task.json", 'r'))

    def cmd_create(self, cmd_data):
        accepted_create_type = ["price", "position"]

        if cmd_data[1] not in accepted_create_type:
            print(f"Cannot create a {cmd_data[1]} task")
            return

        if cmd_data[1] == "price":
            pass

    def cmd_start(self, cmd_data):
        # Implementation for 'start' command
        pass

    def cmd_stop(self, cmd_data):
        # Implementation for 'stop' command
        pass

    def handle_cmd(self, cmd_str: str):
        cmd_data = cmd_str.split(" ")
        command_name = cmd_data[0]

        if command_name not in self.accepted_commands:
            print("Command not accepted")
            return

        self.accepted_commands[command_name](cmd_data[1:])
