from pydantic import BaseModel


class ZeroCrossingItem(BaseModel):
    channel: str
    count: int


class InsightItem(BaseModel):
    id: int

    zero_crossings: list[ZeroCrossingItem]
