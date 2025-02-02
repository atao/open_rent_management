from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.models.base import Base

class Payment(Base):
    __tablename__ = 'payments'

    amount = Column(Integer, nullable=False)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    rental_id = Column(Integer, ForeignKey('rentals.id'), nullable=False)
    is_paid = Column(Boolean, nullable=False)

    tenant = relationship("Tenant", back_populates="payments")
    rental = relationship("Rental", back_populates="payments")