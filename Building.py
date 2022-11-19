from sqlalchemy import Column, String, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from orm_base import Base


class Building(Base):
    __tablename__ = "buildings"
    name = Column("name", String(10), nullable=False, primary_key=True)

    room_list = relationship('Room', back_populates='building', viewonly=False)

    def __int__(self, name: String):
        self.name = name
        self.room_list = []
