import hashlib
from pathlib import Path

import redis

class RedisClient:
	def __init__(self):
		self.client = redis.Redis(decode_responses=True)
		self.pipe = self.client.pipeline()
		self.targets = list(Path("targets").iterdir())

	def write_pairs(self):
		for file in self.targets:
			self.pipe.set(file.name, self.sha256sum(file))
		self.pipe.execute()

	def remove_pairs(self):
		for key in self.client.scan_iter():
			self.pipe.delete(key)
		self.pipe.execute()

	def sha256sum(self, file, buffsize=65536):
		h = hashlib.sha256()
		buffer = bytearray(buffsize)
		buffer_view = memoryview(buffer)

		with open(file, "rb", buffering=0) as f:
			while True:
				chunk = f.readinto(buffer_view)
				if not chunk:
					break
				h.update(buffer_view[:chunk])
			return h.hexdigest()