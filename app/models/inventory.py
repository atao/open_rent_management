from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.property import Property

from .base import Base


class Inventory(Base):
    __tablename__ = "inventories"

    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    property_id: Mapped[int] = mapped_column(Integer, ForeignKey("properties.id"), nullable=False)
    rooms: Mapped[dict[str, str]] = mapped_column(JSON, nullable=True)

    property: Mapped["Property"] = relationship("Property", back_populates="inventories")
