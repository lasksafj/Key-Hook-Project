from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from orm_base import Base


class ReturnKey(Base):
    __tablename__ = "return"
    loan_request_id = Column('loan_request_id', Integer, ForeignKey('loan.request_id'), nullable=False, primary_key=True)
    loss = Column('loss', Boolean, nullable=False)
    return_time = Column('return_time', DateTime, nullable=False)

    loan = relationship("Loan", back_populates="return_key")

    def __int__(self, loan, loss, return_time):
        self.loan_request_id = loan.request_id
        self.loss = loss
        self.return_time = return_time
        self.loan = loan

