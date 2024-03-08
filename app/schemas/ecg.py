from datetime import datetime


from pydantic import BaseModel

from app.schemas.lead import LeadCreate, LeadIteam


class EcgItem(BaseModel):
    id: int
    created_at: datetime
    leads: list[LeadIteam]


class EcgCreate(BaseModel):
    leads: list[LeadCreate]
