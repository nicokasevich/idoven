from pydantic import BaseModel


class LeadIteam(BaseModel):
    id: int
    name: str
    number_of_samples: int
    signal: list[int]


class LeadCreate(BaseModel):
    name: str
    number_of_samples: int
    signal: list[int]
