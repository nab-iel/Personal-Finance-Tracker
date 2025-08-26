from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from dependencies import get_db
from schemas import UserCreate, UserOut

app = FastAPI()

@app.get("/users", response_model=list[UserOut])
async def read_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@app.post("/users", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(username=user.username, email=user.email, password=user.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user