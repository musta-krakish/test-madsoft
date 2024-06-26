from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import scheme, cfg, db

app = FastAPI()

async def get_db() -> AsyncSession:
    async with db.SessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup():
    await db.init_db()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/memes")
async def read_memes(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    memes = await cfg.get_memes(db, skip=skip, limit=limit)
    return memes

@app.get("/memes/{meme_id}")
async def read_meme(meme_id: int, db: AsyncSession = Depends(get_db)):
    db_meme = await cfg.get_meme(db, meme_id=meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail="neme not found")
    return db_meme

@app.post("/memes")
async def create_meme(meme: scheme.MemeCreate, db: AsyncSession = Depends(get_db)):
    return await cfg.create_meme(db=db, meme=meme)

@app.put("/memes/{meme_id}", response_model=scheme.Meme)
async def update_meme(meme_id: int, meme: scheme.MemeUpdate, db: AsyncSession = Depends(get_db)):
    return await cfg.update_meme(db=db, meme_id=meme_id, meme=meme)

@app.delete("/memes/{meme_id}")
async def delete_meme(meme_id: int, db: AsyncSession = Depends(get_db)):
    await cfg.delete_meme(db=db, meme_id=meme_id)
    return {"message": "your meme is killed"}
