from sqlalchemy import Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.payment import Payment
from app.models.property import Property
from app.models.tenant import Tenant
from .base import Base


class Rental(Base):
    __tablename__ = "rentals"

    start_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    rent_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    deposit_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False)
    property_id: Mapped[int] = mapped_column(Integer, ForeignKey("properties.id"), nullable=False)

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="rentals")
    property: Mapped["Property"] = relationship("Property", back_populates="rentals")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="rental")
