from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from orm_base import Base


class HookDoor(Base):
    __tablename__ = 'hook_door'
    hook_number = Column('hook_number', Integer, ForeignKey('hooks.number'), nullable=False, primary_key=True)
    door_room_building_name = Column('door_room_building_name', String(10), ForeignKey('doors.room_building_name'),
                                     nullable=False, primary_key=True)
    door_room_number = Column('door_room_number', Integer, ForeignKey('doors.room_number'), nullable=False, primary_key=True)
    door_name = Column('door_name', String(20), ForeignKey('doors.name'), nullable=False, primary_key=True)

    door = relationship("Door", back_populates='door')
    hook = relationship('Hook', back_populates='hook')

    def __init__(self, hook, door):
        self.hook_number = hook.number
        self.door_room_building_name = door.room_building_name
        self.door_room_number = door.room_number
        self.door_name = door.name
        self.door = door
        self.hook = hook
