import aiohttp
from typing import List, Optional

from random_useragent.random_useragent import Randomize
from .models import (
    User,
    TopResponseItem,
    StartResponse,
    Transaction,
    BalanceResponse,
    RpsType,
    RpsTypes,
    Duel,
    DuelAcceptResponse,
    DuelRejectResponse,
)
import logging

API_URL = "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/"
PROD_SERVER = "https://prod-app7794757-65911b7231ba.pages-ac.vk-apps.com"


class Slaves:
    def __init__(self, app_auth: str) -> None:
        self.app_auth = app_auth
        self.user_agent = Randomize()
        self.me: Optional["User"] = None
        self.slaves: Optional[List["User"]] = None
        self._log = logging.getLogger(__name__)

    async def accept_duel(self, id: int, rps_type: RpsTypes) -> DuelAcceptResponse:
        """Accept duel request (rock-paper-scissors game)

        :param int id: Duel request id
        :param RpsTypes rps_type: Your move

        :return DuelAcceptResponse: Game result
        """
        req = await self.request("GET", "acceptDuel", {"id": id, "rps_type": rps_type})
        return DuelAcceptResponse(**req)

    async def buy_fetter(self, slave_id: int) -> User:
        """Buy fetter to your slave

        :param int slave_id: Id of your slave

        :return User: Slave data
        """
        self._log.debug(f"Buying fetter for {slave_id}")
        req = await self.request("POST", "buyFetter", {"slave_id": slave_id})
        return User(**req)

    async def buy_slave(self, slave_id: int) -> User:
        """Buy slave

        :param int slave_id: ID of the user you want to buy

        :return User: Slave data
        """
        self._log.debug(f"Buying {slave_id}")
        req = await self.request("POST", "buySlave", {"slave_id": slave_id})
        return User(**req)

    async def create_duel(self, user_id: int, amount: int, rps_type: RpsType) -> Duel:
        """Create duel request (rock-paper-scissors game)

        :param int user_id: Opponent id
        :param int amount: Bet
        :param RpsTypes rps_type: Your move

        :return Duel: Game object
        """
        req = await self.request(
            "GET",
            "createDuel",
            {"user_id": user_id, "amount": amount, "rps_type": rps_type},
        )
        return Duel(**req)

    async def groups_as_slaves(self) -> List[User]:
        """Doesn't work yet

        :return List[User]: List of users objects
        """
        req = await self.request("GET", "groupAsSlaves")
        return [User(**item) for item in req["slaves"]]

    async def job_slave(self, name: str, slave_id: int) -> User:
        """Give a job for slave

        :param int slave_id: Id of your slave
        :param str name: Job name

        :return User: Slave data
        """
        self._log.debug(f"Setting job {name} for {slave_id}")
        req = await self.request(
            "POST", "jobSlave", {"name": name, "slave_id": slave_id}
        )
        return User(**req["slave"])

    async def reject_duel(self, id: int) -> DuelRejectResponse:
        """Reject duel request (rock-paper-scissors game)

        :param int id: Duel request id

        :return DuelRejectResponse:
        """
        req = await self.request("POST", "rejectDuel", {"id": id})
        return DuelRejectResponse(**req["slave"])

    async def slave_list(self, id: int) -> List[User]:
        """Get a list of user's slaves

        :param int id: User id

        :return List[User]: List of user's slaves
        """
        req = await self.request("GET", "slaveList", {"id": id})
        return [User(**item) for item in req["slaves"]]

    async def sell_slave(self, slave_id: int) -> User:
        """Sell your slave

        :param int slave_id: ID of slave you want to sell

        :retrun User:
        """
        self._log.debug(f"Selling {slave_id}")
        req = await self.request("POST", "sellSlave", {"slave_id": slave_id})
        return User(**req)

    async def start(self, post=0) -> StartResponse:
        """Start app request

        :param int post: Referral id

        :return StartResponse:
        """
        self._log.debug("Updating data")
        req = StartResponse(**(await self.request("GET", "start", {"post": post})))
        self.me = req.me
        self.slaves = req.slaves
        return req

    async def top_friends(self, ids: List[int]) -> List[TopResponseItem]:
        """Get top of your friends

        :param List[int] ids: Your friends ids

        :return List[TopResponseItem]:
        """
        req = await self.request("POST", "topFriends", {"ids": ids})
        return [TopResponseItem(**item) for item in req["list"]]

    async def top_users(self) -> List[TopResponseItem]:
        """Get top of all users

        :return List[TopResponseItem]:
        """
        req = await self.request("GET", "topUsers")
        return [TopResponseItem(**item) for item in req["list"]]

    async def transations(self) -> List[Transaction]:
        """Get your transations

        :return List[Transaction]:
        """
        req = await self.request("GET", "transations")
        return [Transaction(**item) for item in req["list"]]

    async def transfer_money(self, id: int, amount: int) -> BalanceResponse:
        """Give your money to other user

        :param int id: User id

        :return BalanceResponse: Your balance
        """
        req = await self.request("POST", "user", {"id": id, "amount": amount})
        return BalanceResponse(**req)

    async def user(self, id: int) -> User:
        """Get info of user

        :param int id: User id

        :return User: User data
        """
        req = await self.request("GET", "user", {"id": id})
        return User(**req)

    async def users(self, ids: List[int]) -> List[User]:
        """Get info of users (max 5000)

        :param List[int] ids: IDs of users

        :return List[User]: List of users data
        """
        req = await self.request("POST", "user", {"ids": ids})
        return [User(**item) for item in req["users"]]

    async def request(
        self, method: str, path: str, data: dict = None
    ) -> Optional[dict]:
        params = {"params": data} if method == "GET" else {"json": data}
        headers = {
            "authorization": "Bearer " + self.app_auth,
            "content_type": "application/json",
            "user-agent": self.user_agent.random_agent("desktop", "windows"),
            "origin": PROD_SERVER,
            "referer": PROD_SERVER,
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.request("OPTIONS", API_URL + path):
                async with session.request(
                    method, API_URL + path, **params
                ) as response:
                    res = await response.json()
                    if "error" in res:
                        raise Exception(res["error"])
                    return res


__all__ = ["Slaves"]
