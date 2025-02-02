import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

# Base = declarative_base()

class Tenant(Base):
    __tablename__ = 'tenants'

    firstname = Column(String, index=True)
    surname = Column(String, index=True)
    description = Column(String, nullable=True)
    date_of_birth = Column(DateTime, default=datetime.datetime.utcnow)
    version = Column(Integer, default=1)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    adress = relationship("Adress", back_populates="tenants")
    guarantors = relationship("Guarantor", back_populates="tenant")
    rentals = relationship("Rental", back_populates="tenant")
    payments = relationship("Payment", back_populates="tenant")
    user = relationship("User", back_populates="tenants")
