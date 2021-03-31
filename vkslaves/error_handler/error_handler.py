import json
from typing import Any

from errors import (
    AppError,
    BuyFloodError,
    FetterFloodError,
    FloodError,
    JobFloodError,
    NotEnoughMoneyError,
    NotYourSlaveError,
    SellFloodError,
    SlaveAreLockedError,
)


class ErrorHandler:
    def check(response: str) -> Any:
        if "<html" in response:
            raise AppError("HTML was received")

        data = json.loads(response)

        if "error" not in data:
            return data

        elif (
            "SalveAreLocked"  # "Salve"? HappySanta, are you serious?
            in data["error"]
        ):
            raise SlaveAreLockedError

        elif "NotYouSlave" in data["error"]:
            raise NotYourSlaveError

        elif "Money" in data["error"]:
            raise NotEnoughMoneyError

        elif "ErrFloodBuy" in data["error"]:
            raise BuyFloodError

        elif "ErrFloodJob" in data["error"]:
            raise JobFloodError

        elif "ErrFloodSell" in data["error"]:
            SellFloodError

        elif "ErrFloodFetter" in data["error"]:
            raise FetterFloodError

        elif "ErrFlood" in data["error"]:
            raise FloodError(data)

        else:
            raise AppError(data)


__all__ = ["ErrorHandler"]
