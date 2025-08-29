from sqlalchemy import Column, Integer, Numeric, Date

from app.database import Base

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric, index=True)
    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)
    owner_id = Column(Integer, index=True)
    category_id = Column(Integer, index=True)