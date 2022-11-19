from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from orm_base import Base
from Loan import Loan


class Key(Base):
    __tablename__ = "keys"
    number = Column("number", Integer, nullable=False, primary_key=True)
    hook_number = Column('hook_number', Integer, ForeignKey('hooks.number'), nullable=False)

    hook = relationship("Hook", back_populates="key_list")
    loan_list: [Loan] = relationship('Loan', back_populates='key', viewonly=False, cascade="all, delete, delete-orphan")

    def __int__(self, number, hook):
        self.number = number
        self.hook_number = hook.number
        self.hook = hook
        self.loan_list = []

    def add_request(self, request):
        for loan in self.loan_list:
            if loan == request.loan:
                print('Error add_request')
                return
        loan = Loan(key=self, request=request)
        self.loan_list.append(loan)
        request.loan = loan
