from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Property(Base):
    __tablename__ = 'properties'

    name = Column(String, index=True)
    description = Column(String, nullable=True)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    property_manager_id = Column(Integer, ForeignKey('property_managers.id'))

    address = relationship("Address", back_populates="properties")
    property_manager = relationship("PropertyManager", back_populates="properties")
    rentals = relationship("Rental", back_populates="property")
