
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

class PropertyManager(Base):
    __tablename__ = 'property_managers'

    firstname: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey('addresses.id'), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)

    address: Mapped["Address"] = relationship("Address", back_populates="property_managers")
    user: Mapped["User"] = relationship("User", back_populates="property_managers")
    properties: Mapped[list["Property"]] = relationship("Property", back_populates="property_manager")