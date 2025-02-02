from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from app.models.base import Base

# Base = declarative_base()

class Rental(Base):
    __tablename__ = 'rentals'

    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    property_id = Column(Integer, ForeignKey('properties.id'), nullable=False)
    description = Column(String, nullable=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    rent_amount = Column(Float, nullable=False)
    deposit_amount = Column(Float, nullable=False)

    tenant = relationship('Tenant', back_populates='rentals')
    property = relationship('Property', back_populates='rentals')
    payments = relationship("Payment", back_populates="rental")
