from datetime import datetime
from pydantic import BaseModel
from typing import List


class Start(BaseModel):
    duels: list
    just_slave: bool
    me: "User"
    share_url: str
    slaves: List["User"]
    slaves_profit_per_min: int
    steps: bool


class User(BaseModel):
    balance: int
    chicken_mark: bool
    chicken_mark_clean: int
    duel_count: int
    duel_reject: int
    duel_win: int
    fetter_hour: int
    fetter_price: int
    fetter_to: datetime
    id: int
    item_type: str
    job: "Job"
    master_id: int
    price: int
    profit_per_min: int
    rating_position: int
    sale_price: int
    slaves_count: int
    slaves_profit_per_min: int
    steps_at: int
    was_in_app: bool


class Job(BaseModel):
    name: str


class TopItem(BaseModel):
    id: int
    slaves_count: int


Start.update_forward_refs()
User.update_forward_refs()
Job.update_forward_refs()
