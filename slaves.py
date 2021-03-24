import aiohttp
from typing import List, Optional
from models import User, Start, TopItem
import logging

API_URL = "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/"


class Slaves:
    def __init__(self, app_sign: str) -> None:
        self.app_sign = app_sign
        self.me: Optional["User"] = None
        self.slaves: Optional[List["User"]] = None
        self._log = logging.getLogger(__name__)

    async def buy_fetter(self, slave_id: int) -> "User":
        self._log.debug(f"Buying fetter for {slave_id}")
        req = await self.fetch("POST", "buyFetter", {"slave_id": slave_id})
        return User(**req)

    async def buy_slave(self, slave_id: int) -> "User":
        self._log.debug(f"Buying {slave_id}")
        req = await self.fetch("POST", "buySlave", {"slave_id": slave_id})
        return User(**req)

    async def job_slave(self, name: str, slave_id: int) -> "User":
        self._log.debug(f"Setting job {name} for {slave_id}")
        req = await self.fetch("POST", "jobSlave", {"name": name, "slave_id": slave_id})
        return User(**req["slave"])

    async def slave_list(self, id: int) -> List["User"]:
        req = await self.fetch("GET", "slaveList", {"id": id})
        return [User(**item) for item in req["slaves"]]

    async def start(self) -> "Start":
        self._log.debug("Updating data")
        req = Start(**(await self.fetch("GET", "start")))
        self.me = req.me
        self.slaves = req.slaves
        return req

    async def top_friends(self, ids: List[int]) -> List["TopItem"]:
        req = await self.fetch("POST", "topFriends", {"ids": ids})
        return [TopItem(**item) for item in req["list"]]

    async def top_users(self) -> List["TopItem"]:
        req = await self.fetch("GET", "topUsers")
        return [TopItem(**item) for item in req["list"]]

    async def user(self, ids: List[int] = None):
        req = await self.fetch("POST", "user", {"ids": ids})
        return [User(**item) for item in req["users"]]

    async def fetch(self, method: str, path: str, data: dict = None) -> Optional[dict]:
        params = {"params": data} if method == "GET" else {"json": data}
        headers = {
            "authorization": f"Bearer {self.app_sign}",
            "content_type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.459",
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.request(method, API_URL + path, **params) as response:
                res = await response.json()
                if "error" in res:
                    raise Exception(res["error"])
                return res
