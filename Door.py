from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from orm_base import Base
from Room import Room
from HookDoor import HookDoor


class Door(Base):
    __tablename__ = "doors"
    room_building_name = Column('room_building_name', String(10), ForeignKey('rooms.building_name'),
                                nullable=False, primary_key=True)
    room_number = Column("room_number", Integer, ForeignKey('rooms.number'), nullable=False, primary_key=True)
    name = Column('name', String(20), nullable=False, primary_key=True)

    room = relationship("Room", back_populates="door_list")
    hook_door_list: [HookDoor] = relationship('HookDoor', back_populates='door', viewonly=False)

    def __int__(self, room: Room, name: String):
        self.room_building_name = room.building_name
        self.room_number = room.number
        self.name = name
        self.room = room
        self.hook_door_list = []

    def add_hook(self, hook):
        for hook_door in self.hook_door_list:
            if hook_door.hook == hook:
                print('Error add_hook')
                return
        hook_door = HookDoor(hook=hook, door=self)
        self.hook_door_list.append(hook_door)
        hook.hook_door_list.append(hook_door)
