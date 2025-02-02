from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class Inventory(Base):
    __tablename__ = 'inventories'

    name = Column(String, index=True)
    description = Column(String, nullable=True)
    property_id = Column(Integer, ForeignKey('properties.id'), nullable=False)
    rooms = Column(JSON, nullable=True)

    property = relationship("Property", back_populates="inventories")