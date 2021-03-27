from __future__ import annotations
from enum import Enum
from typing import List, Optional, Literal
from pydantic import BaseModel


class Job(BaseModel):
    name: Optional[str] = None


class DuelAcceptResponse(BaseModel):
    win: Optional[bool] = None
    balance: Optional[int] = None


class DuelRejectResponse(BaseModel):
    chicken_mark_clean: Optional[int] = None


class ItemType(Enum):
    user = "user"
    group = "group"


class User(BaseModel):
    item_type: Optional[ItemType] = None
    id: Optional[int] = None
    job: Optional[Job] = None
    master_id: Optional[int]
    profit_per_min: Optional[int] = None
    fetter_to: Optional[int] = None
    fetter_price: Optional[int]
    sale_price: Optional[int]
    chicken_mark: Optional[bool] = None
    price: Optional[int]
    balance: Optional[int] = None
    duel_count: Optional[int]
    duel_win: Optional[int] = None
    duel_reject: Optional[int] = None
    chicken_mark_clean: Optional[int]
    slaves_count: Optional[int] = None
    rating_position: Optional[int] = None
    slaves_profit_per_min: Optional[int]


class Duel(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    price: Optional[int] = None
    created_at: Optional[int] = None


class TransactionType(Enum):
    buy_slave = "buy_slave"
    transfer_to_user = "transfer_to_user"
    other = "other"


class Transaction(BaseModel):
    id: Optional[str] = None
    type: Optional[TransactionType] = None
    text: Optional[str] = None
    object_id: Optional[int] = None
    created_at: Optional[int] = None
    amount: Optional[int] = None


class TransferRequest(BaseModel):
    user_id: Optional[int] = None
    amount: Optional[int] = None


RpsTypes = Literal["rock", "paper", "scissors"]


class RpsType(Enum):
    rock = "rock"
    paper = "paper"
    scissors = "scissors"


class CreateDuelRequest(BaseModel):
    user_id: Optional[int] = None
    amount: Optional[int] = None
    rps_type: Optional[RpsType] = None


class TopResponseItem(BaseModel):
    id: Optional[int] = None
    slaves_count: Optional[int] = None


class StartResponse(BaseModel):
    me: Optional[User] = None
    share_url: Optional[str] = None
    duels: Optional[List[Duel]] = None
    slaves: Optional[List[User]] = None
    slaves_profit_per_min: Optional[int] = None
    just_slave: Optional[bool] = None
