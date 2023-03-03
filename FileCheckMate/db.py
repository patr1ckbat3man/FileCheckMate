import hashlib
from pathlib import Path
from typing import Any

import redis

class RedisClient:
    LOADED = False

    def __init__(self):
        self.client = redis.Redis(decode_responses=True)
        self.pipe = self.client.pipeline()
        self.targets = list(Path("targets").iterdir())

    def write(self, file_config=None) -> None:
        if self.is_empty("targets"):
            print("Target folder cannot be empty.")
            return

        if file_config:
            to_remove = set(file_config)
            new_targets = []

            for file in self.targets:
                if file.name not in to_remove:
                    new_targets.append(file)
            self.targets = new_targets

        self.client.flushall()
        for file in self.targets:
            self.pipe.set(file.name, self.sha256sum(file))
        self.pipe.execute()
        self.LOADED = True
        print("Baseline loaded successfully.")

    def verify(self) -> None:
        if not self.LOADED:
            print("You have to load a baseline first!")
            return

        keys = list(self.client.scan_iter())
        values = []
        for k in keys:
            values.append(self.client.get(k))

        cached_pairs = list(zip(keys, values))

        temp_keys = []
        temp_values = []
        for file in self.targets:
            temp_keys.append(file.name)
            temp_values.append(self.sha256sum(file))
        temp_pairs = list(zip(temp_keys, temp_values))

        print(cached_pairs.sort() == temp_pairs.sort())

    @staticmethod
    def sha256sum(file: Any, buffer_size: int = 65536) -> str:
        h = hashlib.sha256()
        buffer = bytearray(buffer_size)
        buffer_view = memoryview(buffer)

        with open(file, "rb", buffering=0) as f:
            while True:
                chunk = f.readinto(buffer_view)
                if not chunk:
                    break
                h.update(buffer_view[:chunk])
            return h.hexdigest()

    @staticmethod
    def is_empty(folder_path: Any) -> bool:
        return not any(Path(folder_path).iterdir())
