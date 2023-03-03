import sys
from pathlib import Path

from .db import RedisClient
from .prompts import file_config, interval_config

class Monitor:
    def __init__(self):
        self.redis_client = RedisClient()

    def start(self, target_folder: str = "targets") -> None:
        Path(target_folder).mkdir(exist_ok=True)
        self.menu()

    def menu(self) -> None:
        actions = {
            1: lambda: self.redis_client.write(file_config=file_config()),
            2: lambda: None,
            3: lambda: None,
            4: lambda: self.redis_client.verify(),
            5: lambda: sys.exit(0),
        }

        while True:
            print("1 - Load / Reload baseline")
            print("2 - Configure email (Disabled by default)")
            print("3 - Configure logger (Disabled by default)")
            print("4 - Start monitoring")
            print("5 - Stop monitoring and exit")

            try:
                choice = int(input("> "))
                if choice not in actions:
                    print("Invalid choice! Choose from: 1 - 5")
                else:
                    action = actions[choice]
                    action()
            except ValueError:
                print("Wrong data input!")
