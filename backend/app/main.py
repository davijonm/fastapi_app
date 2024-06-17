from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from . import models, schemas, crud
from .database import async_session, database, engine

app = FastAPI()

# Configuração do middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Podemos adicionar outras origems que possam fazer um request
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

async def get_db():
    async with async_session() as session:
        yield session

@app.get("/", response_model=dict)
async def home():
    return {"message": "Home page"}

@app.get("/items/", response_model=List[schemas.Item])
async def read_items(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    items = await crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    db_item = await crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.post("/items/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_item(db, item)