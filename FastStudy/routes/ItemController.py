# routes/ItemController.py
import logging

import beanie
import pymongo
from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError
from typing import List, Optional

from models.ShopItem import ShopItem
from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from auth.dependencies import get_current_user
from models.User import User

router = APIRouter(prefix="/shop", tags=["Shop"])
logger = logging.getLogger("studyshield.routes.shop")


class ShopItemCreate(BaseModel):
    title:       str
    description: Optional[str] = None
    price:       int
    image_url:   str = Field(..., alias="image_url")

    class Config:
        allow_population_by_field_name = True


@router.get("/items", response_model=List[ShopItem])
async def get_shop_items():
    try:
        return await ShopItem.find().to_list()
    except beanie.exceptions.DocumentNotFound as dnfe:
        logger.error("Database document not found", exc_info=dnfe)
        raise HTTPException(status_code=404, detail="Shop items not found")
    except pymongo.errors.PyMongoError as pme:
        logger.error("Database operation failed", exc_info=pme)
        raise HTTPException(status_code=503, detail="Database service unavailable")
    except Exception as e:
        logger.exception("Failed to fetch shop items:" + str(e))
        raise HTTPException(status_code=500, detail="Internal error fetching shop items")


@router.get("/items/{item_id}", response_model=ShopItem)
async def get_shop_item(item_id: str):
    item = await ShopItem.get(PydanticObjectId(item_id))
    if not item:
        logger.warning(f"Shop item not found: {item_id}")
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/items", response_model=ShopItem, status_code=201)
async def create_shop_item(item_data: ShopItemCreate):
    try:
        item = ShopItem(**item_data.dict(by_alias=True))
        await item.insert()
        return item
    except ValidationError as ve:
        logger.error("Payload validation failed", exc_info=ve)
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        logger.exception("Failed to create shop item")
        raise HTTPException(status_code=500, detail="Internal error creating shop item")


@router.post("/items/seed-default")
async def seed_default_items(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        logger.warning(f"Unauthorized seed-default attempt by {current_user.email}")
        raise HTTPException(status_code=403, detail="Admin access required")

    default_items = [
        ShopItem(
            title="Study Shield Premium",
            description="Unlock all premium features of Study Shield",
            price=100,
            image_url="https://images.unsplash.com/photo-1434030216411-0b793f4b4173",
        ),
    ]
    await ShopItem.insert_many(default_items)
    return {"message": "Default shop items seeded"}
