from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

class Payment(Base):
    __tablename__ = 'payments'

    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey('tenants.id'), nullable=False)
    rental_id: Mapped[int] = mapped_column(Integer, ForeignKey('rentals.id'), nullable=False)
    is_paid: Mapped[bool] = mapped_column(Boolean, nullable=False)

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="payments")
    rental: Mapped["Rental"] = relationship("Rental", back_populates="payments")