from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

# Base = declarative_base()

class PropertyManager(Base):
    __tablename__ = 'property_managers'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    adress = relationship("Adress", back_populates="property_managers")
    user = relationship("User", back_populates="property_managers")
    properties = relationship("Property", back_populates="property_manager")
