from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models, scheme

async def get_memes(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Meme).offset(skip).limit(limit))
    return result.scalars().all()

async def get_meme(db: AsyncSession, meme_id: int):
    result = await db.execute(select(models.Meme).where(models.Meme.id == meme_id))
    return result.scalars().first()

async def create_meme(db: AsyncSession, meme: scheme.MemeCreate):
    db_meme = models.Meme(title=meme.title, description=meme.description, image_url=meme.image_url)
    db.add(db_meme)
    await db.commit()
    await db.refresh(db_meme)
    return db_meme

async def update_meme(db: AsyncSession, meme_id: int, meme: scheme.MemeUpdate):
    result = await db.execute(select(models.Meme).where(models.Meme.id == meme_id))
    db_meme = result.scalars().first()
    if db_meme:
        db_meme.title = meme.title
        db_meme.description = meme.description
        db_meme.image_url = meme.image_url
        await db.commit()
        await db.refresh(db_meme)
    return db_meme

async def delete_meme(db: AsyncSession, meme_id: int):
    result = await db.execute(select(models.Meme).where(models.Meme.id == meme_id))
    db_meme = result.scalars().first()
    if db_meme:
        await db.delete(db_meme)
        await db.commit()
