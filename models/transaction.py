from sqlalchemy import Column, Integer, Boolean, Numeric, Text, Date

from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric, index=True)
    date = Column(Date, index=True)
    description = Column(Text)
    is_income = Column(Boolean, index=True)
    owner_id = Column(Integer, index=True)
    category_id = Column(Integer, index=True)