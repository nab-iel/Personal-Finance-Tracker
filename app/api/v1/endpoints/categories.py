from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_

from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.dependencies import get_db
from app.models.user import User
from app.models.category import Category
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
        category_in: CategoryCreate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    """Create a new category for the current user."""
    result = await db.execute(
        select(Category)
        .filter(
            Category.name == category_in.name,
            or_(Category.owner_id == current_user.id, Category.owner_id.is_(None))
        )
    )
    existing_category = result.scalars().first()

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A category with this name already exists.",
        )

    db_category = Category(
        **category_in.model_dump(),
        owner_id=current_user.id
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    """Retrieve categories for the current user (including global categories)."""
    result = await db.execute(
        select(Category)
        .filter(or_(Category.owner_id == current_user.id, Category.owner_id.is_(None)))
    )
    return result.scalars().all()

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
        category_id: int,
        category_in: CategoryUpdate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    """Update a category owned by the current user."""
    result = await db.execute(
        select(Category)
        .where(Category.id == category_id)
    )
    db_category = result.scalar_one_or_none()

    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found or you do not have permission to edit it.",
        )

    if db_category.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update categories you own.",
        )

    update_data = category_in.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)

    await db.commit()
    await db.refresh(db_category)
    return db_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
        category_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """Delete a category owned by the current user."""
    result = await db.execute(
        select(Category)
        .where(Category.id == category_id, Category.owner_id == current_user.id)
    )
    db_category = result.scalar_one_or_none()

    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    if db_category.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete categories you own.",
        )

    await db.delete(db_category)
    await db.commit()
    return None