import hashlib
from pathlib import Path
from typing import Any, List

import redis

from .dev.log import logger

class RedisClient:
    LOADED = False

    def __init__(self):
        self.targets = list(Path("targets").iterdir())
        self.client = None
        self.pipe = None
        self._connect()

    def _connect(self, host: str = "localhost", port: int = 6379) -> None:
        self.client = redis.Redis(host=host, port=port, decode_responses=True)
        self.pipe = self.client.pipeline()

    def write(self, file_config: List[str] = None) -> None:
        if self.is_empty("targets"):
            print("[MONITOR] Target folder cannot be empty.")
            return

        if self.check_baseline():
            self.clear()

        if file_config:
            target_names = [f.name for f in self.targets]
            for file_name in file_config:
                if file_name not in target_names:
                    print("[MONITOR] Some of the file(s) you have specified aren't present in the target directory!")
                    return

            new_targets = []

            for file in self.targets:
                if file.name not in file_config:
                    new_targets.append(file)
            self.targets = new_targets

        for file in self.targets:
            file_hash = self.sha256sum(file)
            if file_hash:
                self.pipe.set(file.name, file_hash)
        self.pipe.execute()
        self.LOADED = True
        logger.info("Baseline loaded successfully.")

    def verify(self) -> None:
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

        if sorted(cached_pairs) == sorted(temp_pairs):
            logger.info("No files have changed.")
        else:
            for i, (cached_key, cached_value) in enumerate(sorted(cached_pairs)):
                temp_key, temp_value = sorted(temp_pairs)[i]
                if cached_key != temp_key or cached_value != temp_value:
                    logger.info(f"The integrity of {temp_key} has changed.")

    def check_baseline(self) -> bool:
        if not self.LOADED:
            return False
        return True

    def clear(self) -> None:
        self.client.flushall()
        self.LOADED = False
        logger.info("Baseline cleared successfully.")

    @staticmethod
    def sha256sum(file: Any, buffer_size: int = 65536) -> str:
        h = hashlib.sha256()
        buffer = bytearray(buffer_size)
        buffer_view = memoryview(buffer)

        try:
            with open(file, "rb", buffering=0) as f:
                while True:
                    chunk = f.readinto(buffer_view)
                    if not chunk:
                        break
                    h.update(buffer_view[:chunk])
                return h.hexdigest()
        except FileNotFoundError:
            pass

    @staticmethod
    def is_empty(folder_path: Any) -> bool:
        return not any(Path(folder_path).iterdir())
