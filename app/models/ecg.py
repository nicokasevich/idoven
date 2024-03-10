from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.insight import Insight
    from app.models.lead import Lead


class Ecg(Base):
    __tablename__ = "ecgs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    leads: Mapped[list["Lead"]] = relationship(back_populates="ecg")

    insight: Mapped["Insight"] = relationship(back_populates="ecg", uselist=False)

    def __repr__(self) -> str:
        return f"<Ecg {self.id}>"
