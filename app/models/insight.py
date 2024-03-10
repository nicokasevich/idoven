from typing import TYPE_CHECKING

from sqlalchemy import JSON, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.schemas.insight import ZeroCrossingItem

if TYPE_CHECKING:
    from app.models.ecg import Ecg


class Insight(Base):
    __tablename__ = "insights"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    zero_crossings: Mapped[list[ZeroCrossingItem]] = mapped_column(JSON, default=list)

    ecg_id: Mapped[int] = mapped_column(Integer, ForeignKey("ecgs.id"), index=True)
    ecg: Mapped["Ecg"] = relationship(back_populates="insight")

    def __repr__(self) -> str:
        return f"<Insight {self.id}>"
