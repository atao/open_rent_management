from typing import List, TYPE_CHECKING
from sqlalchemy import Boolean, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.property_manager import PropertyManager
from .base import Base

if TYPE_CHECKING:
    from app.models.tenant import Tenant


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, index=True, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    # TODO ADD ROLE

    tenants: Mapped[List["Tenant"]] = relationship("Tenant", back_populates="user")
    property_managers: Mapped[List["PropertyManager"]] = relationship("PropertyManager", back_populates="user")
