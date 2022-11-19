from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from orm_base import Base


class Loan(Base):
    __tablename__ = "loan"
    key_number = Column("key_number", Integer, ForeignKey('keys.number'), nullable=False)
    request_id = Column('request_id', Integer, ForeignKey('requests.id'), nullable=False, primary_key=True)

    key = relationship("Key", back_populates="loan_list")
    request = relationship('Request', back_populates='loan', cascade="all, delete, delete-orphan", single_parent=True)
    return_key = relationship('ReturnKey', back_populates='loan', cascade="all, delete, delete-orphan",
                              single_parent=True)

    def __int__(self, key, request):
        self.key_number = key.number
        self.request_id = request.id
        self.key = key
        self.request = request

