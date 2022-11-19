from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from orm_base import Base
from HookDoor import HookDoor
from Key import Key


class Hook(Base):
    __tablename__ = "hooks"
    number = Column("number", Integer, nullable=False, primary_key=True)

    key_list: [Key] = relationship("Key", back_populates="hook", viewonly=False, cascade="all, delete, delete-orphan")
    hook_door_list: [HookDoor] = relationship('HookDoor', back_populates='hook', viewonly=False,
                                              cascade="all, delete, delete-orphan")

    def __int__(self, number: Integer):
        self.number = number
        self.hook_door_list = []
        self.key_list = []

    def add_door(self, door):
        for hook_door in self.hook_door_list:
            if hook_door.door == door:
                print('Error add_door')
                return
        hook_door = HookDoor(hook=self, door=door)
        self.hook_door_list.append(hook_door)
        door.hook_door_list.append(hook_door)

    # def add_key(self, number):
    #     for key in self.key_list:
    #         if key.number == number:
    #             print('Error add_key')
    #             return
    #     key = Key(number=number)
    #     self.key_list.append(key)
