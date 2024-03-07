from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.lead import Lead


class Ecg(Base):
    __tablename__ = "ecgs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    leads: Mapped["Lead"] = relationship(back_populates="ecg")

    def __repr__(self) -> str:
        return f"<Ecg {self.id}>"
