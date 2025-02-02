from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

class Property(Base):
    __tablename__ = 'properties'

    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey('addresses.id'), nullable=True)
    property_manager_id: Mapped[int] = mapped_column(Integer, ForeignKey('property_managers.id'), nullable=False)

    address: Mapped["Address"] = relationship("Address", back_populates="properties")
    property_manager: Mapped["PropertyManager"] = relationship("PropertyManager", back_populates="properties")
    inventories: Mapped[list["Inventory"]] = relationship("Inventory", back_populates="property")
    rentals: Mapped[list["Rental"]] = relationship("Rental", back_populates="property")