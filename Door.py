from sqlalchemy import Column, String, Integer, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship


from orm_base import Base
from Room import Room


class Door(Base):
    __tablename__ = "doors"
    room_building_name = Column('room_building_name', String(10),
                                nullable=False, primary_key=True)
    room_number = Column("room_number", Integer, nullable=False, primary_key=True)
    name = Column('name', String(20), nullable=False, primary_key=True)

    __table_args__ = (ForeignKeyConstraint([room_building_name, room_number],
                                           [Room.building_name, Room.number]),
                      {})

    room = relationship("Room", back_populates="door_list")
    hook_door_list = relationship('HookDoor', back_populates='door', viewonly=False,
                                  cascade="all, delete, delete-orphan")

    def __int__(self, room, name: String):
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
        from HookDoor import HookDoor
        hook_door = HookDoor(hook=hook, door=self)
        self.hook_door_list.append(hook_door)
        hook.hook_door_list.append(hook_door)
