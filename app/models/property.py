from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.models.address import Address
    from app.models.inventory import Inventory
    from app.models.property_manager import PropertyManager
    from app.models.rental import Rental

from .base import Base


class Property(Base):
    __tablename__ = "properties"

    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey("addresses.id"), nullable=True)
    property_manager_id: Mapped[int] = mapped_column(Integer, ForeignKey("property_managers.id"), nullable=False)

    address: Mapped["Address"] = relationship("Address", back_populates="properties")
    property_manager: Mapped["PropertyManager"] = relationship("PropertyManager", back_populates="properties")
    inventories: Mapped[List["Inventory"]] = relationship("Inventory", back_populates="property")
    rentals: Mapped[List["Rental"]] = relationship("Rental", back_populates="property")
