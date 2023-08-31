from typing import Dict, Any
import json

import aiofiles


class Config:
    """A simple config manager so settings persist across restarts."""

    def __init__(self, path: str, defaults: Dict[str, Any]):
        self.path = path
        self.defaults = defaults
        self._data: Dict[str, Any] = {}

    async def load(self):
        try:
            async with aiofiles.open(self.path, mode='r') as f:
                contents = await f.read()
                self._data = json.loads(contents)
                await f.close()
        except FileNotFoundError:
            self._data = self.defaults.copy()
            await self.save()

    async def save(self):
        async with aiofiles.open(self.path, mode='w') as f:
            await f.write(json.dumps(self._data))
            await f.close()

    def set(self, key: str, val: Any):
        self._data[key] = val

    def get(self, key: str) -> Any:
        return self._data.get(key)
