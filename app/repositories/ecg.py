from typing import Optional, Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Ecg, Lead
from app.schemas.ecg import EcgCreate


class EcgRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def all_by_user(self, user_id: int) -> Sequence[Ecg]:
        stmt = select(Ecg).where(Ecg.user_id == user_id)
        return self.db.scalars(stmt).all()

    def get(self, id: int) -> Optional[Ecg]:
        stmt = select(Ecg).where(Ecg.id == id)
        return self.db.scalar(stmt)

    def create(self, request: EcgCreate, user_id: int) -> Ecg:
        ecg = Ecg(
            leads=[Lead(**lead.model_dump()) for lead in request.leads], user_id=user_id
        )
        self.db.add(ecg)
        self.db.commit()
        self.db.refresh(ecg)
        return ecg

    def update(self, ecg: Ecg) -> Ecg:
        self.db.add(ecg)
        self.db.commit()
        self.db.refresh(ecg)
        return ecg
