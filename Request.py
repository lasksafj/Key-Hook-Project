from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from Loan import Loan
from orm_base import Base
from Room import Room


class Request(Base):
    __tablename__ = 'requests'
    employee_employee_id = Column('employee_employee_id', Integer, ForeignKey('employees.employee_id'), nullable=False)
    room_building_name = Column('room_building_name', String(10), nullable=False)
    room_number = Column('room_number', Integer, nullable=False)
    request_time = Column('request_time', DateTime, nullable=False)
    id = Column('id', Integer, primary_key=True)
    table_args = (UniqueConstraint("employee_employee_id", "room_building_name", "room_number", "request_time",
                                   name="request_uk_01"))
    __table_args__ = (ForeignKeyConstraint([room_building_name, room_number],
                                           [Room.building_name, Room.number]),
                      {})

    employee = relationship("Employee", back_populates='request_list')
    room = relationship("Room", back_populates='request_list')
    loan = relationship('Loan', back_populates='request', cascade="all, delete, delete-orphan", single_parent=True)

    def __init__(self, employee, room, request_time: DateTime):
        self.employee_employee_id = employee.employee_id
        self.room_building_name = room.building_name
        self.room_number = room.number
        self.request_time = request_time
        self.employee = employee
        self.room = room

    def grant_key(self, key):
        if self.loan:
            return
        loan = Loan(key=key, request=self)
        key.loan_list.append(loan)
        self.loan = [loan]


