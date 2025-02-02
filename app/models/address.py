from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
class Address(Base):
    __tablename__ = 'addresses'

    street: Mapped[str] = mapped_column(String, index=True)
    city: Mapped[str] = mapped_column(String, index=True)
    state: Mapped[str] = mapped_column(String, index=True)
    postal_code: Mapped[str] = mapped_column(String, index=True)
    country: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)

    tenants: Mapped[list["Tenant"]] = relationship("Tenant", back_populates="address")
    properties: Mapped[list["Property"]] = relationship("Property", back_populates="address")
    guarantors: Mapped[list["Guarantor"]] = relationship("Guarantor", back_populates="address")
    property_managers: Mapped[list["PropertyManager"]] = relationship("PropertyManager", back_populates="address")