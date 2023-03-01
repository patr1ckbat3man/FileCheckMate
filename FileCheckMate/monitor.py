import hashlib
from pathlib import Path

from .db import RedisClient

class Monitor:
	def __init__(self):
		self.redis_client = RedisClient()

	def start(self, target_folder="targets"):
		Path(target_folder).mkdir(exist_ok=True)
		self.menu()

		if self.folder_empty(target_folder):
			print("Target folder cannot be empty.")
			return

		self.redis_client.remove_pairs()
			
	def exit(self):
		pass

	def menu(self):
		actions = {
		1: lambda: self.redis_client.write_pairs(),
		2: lambda: None,
		3: lambda: None,
		4: lambda: None,
		5: lambda: None,
		6: lambda: None,
		"default": lambda: print("Wrong choice.")
		}

		print("1 - Load / Reload baseline")
		print("2 - Reload baseline")
		print("3 - ")
		print("4 - ")
		print("5 - Start monitoring")
		print("6 - Stop monitoring")

		try:
			choice = int(input("> "))
			action = actions.get(choice, actions["default"])
			action()
		except ValueError:
			print("Wrong data input.")

	def folder_empty(self, folder_path):
		return not any(Path(folder_path).iterdir())