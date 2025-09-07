from sqlalchemy import Column, Integer, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric, index=True)
    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)

    owner = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")