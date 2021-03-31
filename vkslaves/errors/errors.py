class AppError(Exception):
    pass


class FloodError(AppError):
    pass


class FetterFloodError(FloodError):
    pass


class BuyFloodError(FloodError):
    pass


class SellFloodError(FloodError):
    pass


class JobFloodError(FloodError):
    pass


class NotYourSlaveError(AppError):
    pass


class SlaveAreLockedError(AppError):
    pass


class NotEnoughMoneyError(AppError):
    pass


__all__ = [
    "AppError",
    "FloodError",
    "BuyFloodError",
    "JobFloodError",
    "SellFloodError",
    "FetterFloodError",
    "NotYourSlaveError",
    "SlaveAreLockedError",
    "NotEnoughMoneyError",
]
