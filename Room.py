from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from orm_base import Base
from Building import Building


class Room(Base):
    __tablename__ = "rooms"
    building_name = Column("building_name", String(10), ForeignKey('buildings.name'), nullable=False, primary_key=True)
    number = Column("number", Integer, nullable=False, primary_key=True)

    request_list = relationship("Request", back_populates="room", viewonly=False, cascade="all, delete, delete-orphan")
    door_list = relationship("Door", back_populates="room", viewonly=False, cascade="all, delete, delete-orphan")
    building = relationship('Building', back_populates='room_list')

    def __int__(self, building: Building, number: Integer):
        self.building_name = building.name
        self.number = number
        self.request_list = []
        self.door_list = []
        self.building = building

    # def add_door(self, door_name):
    #     for door in self.door_list:
    #         if door.room_building_name == self.building_name and \
    #                 door.room_number == self.number and door.name == door_name:
    #             print("Error add_door: door with current room is already exist")
    #             return
    #     door = Door(room_building_name=self.building_name, room_number=self.number, name=door_name)
    #     self.door_list.append(door)
