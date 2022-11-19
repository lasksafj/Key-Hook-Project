from sqlalchemy import Column, String, Integer, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from orm_base import Base
from Door import Door


class HookDoor(Base):
    __tablename__ = 'hook_door'
    hook_number = Column('hook_number', Integer, ForeignKey('hooks.number'), nullable=False, primary_key=True)
    door_room_building_name = Column('door_room_building_name', String(10),
                                     nullable=False, primary_key=True)
    door_room_number = Column('door_room_number', Integer, nullable=False, primary_key=True)
    door_name = Column('door_name', String(20), nullable=False, primary_key=True)

    __table_args__ = (ForeignKeyConstraint([door_room_building_name, door_room_number, door_name],
                                           [Door.room_building_name, Door.room_number, Door.name]),
                      {})

    door = relationship('Door', back_populates='hook_door_list')
    hook = relationship('Hook', back_populates='hook_door_list')

    def __init__(self, hook, door):
        self.hook_number = hook.number
        self.door_room_building_name = door.room_building_name
        self.door_room_number = door.room_number
        self.door_name = door.name
        self.door = door
        self.hook = hook
