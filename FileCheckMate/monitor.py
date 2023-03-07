import time
import schedule
import os
import sys
from pathlib import Path

from .db import RedisClient
from .prompts import file_config, interval_config
from .dev.log import logger

class Monitor:

    def __init__(self):
        self.redis_client = RedisClient()
        self.running = False

    def start(self, target_folder: str = "targets") -> None:
        Path(target_folder).mkdir(exist_ok=True)
        self.menu()

    def menu(self) -> None:
        actions = {
            1: lambda: self.redis_client.write(file_config=file_config()),
            2: lambda: self.start_verification(),
            3: lambda: self.on_exit(),
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
        if not self.redis_client.check_baseline():
            print("[MONITOR] You have to load a baseline first!")
            return

        try:
            interval = interval_config()
            os.system("cls||clear")
            print("[MONITOR] Press CTRL + C to stop monitoring.")

            if self.running:
                schedule.clear()

            schedule.every(interval).seconds.do(self.redis_client.verify)

            while True:
                schedule.run_pending()
                self.running = True
                time.sleep(1)
        except KeyboardInterrupt:
            print()
            logger.info("Monitoring stopped.")

    def on_exit(self):
        logger.info("Script terminated.")
        self.redis_client.clear()
        sys.exit(0)
