from typing import TYPE_CHECKING

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.ecg import Ecg


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    number_of_samples: Mapped[int] = mapped_column(Integer)
    signal: Mapped[list[int]] = mapped_column(JSON, default=list)

    ecg_id: Mapped[int] = mapped_column(Integer, ForeignKey("ecgs.id"), index=True)
    ecg: Mapped["Ecg"] = relationship(back_populates="leads")

    def __repr__(self) -> str:
        return f"<Lead {self.name}>"
