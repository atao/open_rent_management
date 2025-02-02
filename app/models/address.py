from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class Address(Base):
    __tablename__ = 'addresses'

    street = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    postal_code = Column(String, index=True)
    country = Column(String, index=True)
    description = Column(String, nullable=True)

    tenants = relationship("Tenant", back_populates="adress")
    properties = relationship("Property", back_populates="adress")
    guarantors = relationship("Guarantor", back_populates="adress")
    property_managers = relationship("PropertyManager", back_populates="address")
