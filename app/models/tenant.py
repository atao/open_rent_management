import datetime
from sqlalchemy import DateTime, ForeignKey, String, event
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

class Tenant(Base):
    __tablename__ = 'tenants'

    firstname: Mapped[str] = mapped_column(String, index=True)
    surname: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    date_of_birth: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    email: Mapped[str] = mapped_column(String, index=True)
    phone: Mapped[str] = mapped_column(String, index=True)
    address_id: Mapped[int] = mapped_column(ForeignKey('addresses.id'), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)

    address: Mapped["Address"] = relationship("Address", back_populates="tenants")
    guarantors: Mapped[list["Guarantor"]] = relationship("Guarantor", back_populates="tenant")
    rentals: Mapped[list["Rental"]] = relationship("Rental", back_populates="tenant")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="tenant")
    user: Mapped["User"] = relationship("User", back_populates="tenants")
