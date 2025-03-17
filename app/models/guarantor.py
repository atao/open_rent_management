import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.address import Address
from app.models.tenant import Tenant
from .base import Base


class Guarantor(Base):
    __tablename__ = "guarantors"

    firstname: Mapped[str] = mapped_column(String, index=True)
    surname: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    date_of_birth: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    email: Mapped[str] = mapped_column(String, index=True)
    phone: Mapped[str] = mapped_column(String, index=True)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"), nullable=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=True)

    address: Mapped["Address"] = relationship("Address", back_populates="guarantors")
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="guarantors")
