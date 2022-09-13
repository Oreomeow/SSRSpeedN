import json
import subprocess
import sys
from typing import Any, Dict

import aiofiles
from loguru import logger

from ssrspeed.launchers import BaseClient
from ssrspeed.paths import KEY_PATH

CLIENTS_DIR = KEY_PATH["clients"]


# CONFIG_FILE = KEY_PATH["config.json"]


class V2Ray(BaseClient):
    def __init__(self, file: str):
        super(V2Ray, self).__init__()
        self.config_file: str = f"{file}.json"

    async def start_client(self, config: Dict[str, Any], debug=False):
        self._config = config
        async with aiofiles.open(self.config_file, "w+", encoding="utf-8") as f:
            await f.write(json.dumps(self._config))

        if self._process is None:

            if V2Ray._platform == "Windows":
                if debug:
                    self._process = subprocess.Popen(
                        [
                            f"{CLIENTS_DIR}v2ray-core/v2ray.exe",
                            "--config",
                            self.config_file,
                        ]
                    )
                else:
                    self._process = subprocess.Popen(
                        [
                            f"{CLIENTS_DIR}v2ray-core/v2ray.exe",
                            "--config",
                            self.config_file,
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                logger.info(
                    f'Starting v2ray-core with server {config["server"]}:{config["server_port"]}'
                )

            elif V2Ray._platform == "Linux" or V2Ray._platform == "MacOS":
                if debug:
                    self._process = subprocess.Popen(
                        [
                            f"{CLIENTS_DIR}v2ray-core/v2ray",
                            "--config",
                            self.config_file,
                        ]
                    )
                else:
                    self._process = subprocess.Popen(
                        [
                            f"{CLIENTS_DIR}v2ray-core/v2ray",
                            "--config",
                            self.config_file,
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                logger.info(
                    f'Starting v2ray-core with server {config["server"]}:{config["server_port"]}'
                )

            else:
                logger.critical(
                    "Your system does not support it. Please contact the developer."
                )
                sys.exit(1)
