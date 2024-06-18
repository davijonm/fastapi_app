from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def get_item(db: AsyncSession, item_id: int):
    result = await db.execute(select(models.Item).filter(models.Item.id == item_id))
    return result.scalars().first()

async def get_items(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Item).offset(skip).limit(limit))
    return result.scalars().all()

async def create_item(db: AsyncSession, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
