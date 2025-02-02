from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(Base):
    __tablename__ = 'users'
    email = Column(String, index=True)
    password = Column(String, index=True)

    tenants = relationship("Tenant", back_populates="user")
    property_managers = relationship("PropertyManager", back_populates="user")
