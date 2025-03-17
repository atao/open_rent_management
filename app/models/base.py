from sqlalchemy import Column, DateTime, Integer, event
from sqlalchemy.orm import DeclarativeBase
import datetime


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    version = Column(Integer, default=1)

    @classmethod
    def __tablename__(cls):
        return cls.__name__.lower() + "s"


@event.listens_for(Base, "before_insert", propagate=True)
def set_date_created(mapper, connection, target):
    target.date_created = datetime.datetime.utcnow()
    target.date_updated = datetime.datetime.utcnow()
    target.version = 1


@event.listens_for(Base, "before_update", propagate=True)
def set_date_updated(mapper, connection, target):
    target.date_updated = datetime.datetime.utcnow()
    target.version = target.version + 1
