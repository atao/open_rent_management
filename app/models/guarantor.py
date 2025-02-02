import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

# Base = declarative_base()

class Guarantor(Base):
    __tablename__ = 'guarantors'

    firstname = Column(String, index=True)
    surname = Column(String, index=True)
    description = Column(String, nullable=True)
    date_of_birth = Column(DateTime, default=datetime.datetime.utcnow)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    tenant_id = Column(Integer, ForeignKey('tenants.id'))

    tenant = relationship("Tenant", back_populates="guarantors")
    address = relationship("Address", back_populates="guarantors")
