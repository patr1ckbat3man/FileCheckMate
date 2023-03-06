import sched
import time
import os
import sys
from pathlib import Path

from .db import RedisClient
from .prompts import file_config, interval_config
from .dev.log import logger

class Monitor:

    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.redis_client = RedisClient()

    def start(self, target_folder: str = "targets", log_folder: str = "logs") -> None:
        Path(target_folder).mkdir(exist_ok=True)
        Path(log_folder).mkdir(exist_ok=True)
        self.menu()

    def menu(self) -> None:
        actions = {
            1: lambda: self.redis_client.write(file_config=file_config()),
            2: lambda: self.start_verification(),
            3: lambda: sys.exit(0),
        }

        while True:
            print("1 - Load / Reload baseline")
            print("2 - Start monitoring")
            print("3 - Exit")

            try:
                choice = int(input("> "))
                if choice not in actions:
                    print("Invalid choice! Choose from: 1 - 3")
                else:
                    action = actions[choice]
                    action()
            except ValueError:
                print("Wrong data input!")

    def start_verification(self) -> None:
        try:
            interval = interval_config()
            os.system("cls||clear")
            print("[MONITOR] Press CTRL + C to stop monitoring.")

            self.scheduler.enter(interval, 1, self.redis_client.verify, (interval,))
            self.scheduler.run()
        except KeyboardInterrupt:
            print()
            logger.info("Monitoring stopped.")
