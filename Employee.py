from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from orm_base import Base
from Request import Request


class Employee(Base):
    __tablename__ = "employees"
    name = Column("name", String(60), nullable=False)
    employee_id = Column("employee_id", Integer, nullable=False, primary_key=True)

    request_list: [Request] = relationship("Request", back_populates="employee", viewonly=False,
                                           cascade="all, delete, delete-orphan")

    def __int__(self, name: String, employee_id: Integer):
        self.employee_id = employee_id
        self.name = name
        self.request_list = []

    def request_room(self, room, request_time):
        for request in self.request_list:
            if request.room == room and request.request_time == request_time:
                print("Error request_room: current employee has already requested the room at given time")
                return
        request = Request(employee=self, room=room, request_time=request_time)
        room.request_list.append(request)
        self.request_list.append(request)
        return request
