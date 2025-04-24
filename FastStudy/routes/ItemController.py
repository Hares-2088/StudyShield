from fastapi import APIRouter, HTTPException, Depends
from models.ShopItem import ShopItem
from typing import List, Optional
from beanie import PydanticObjectId
from auth.dependencies import get_current_user
from models.User import User

router = APIRouter(prefix="/shop", tags=["Shop"])


# All shop items - public
@router.get("/items", response_model=List[ShopItem])
async def get_shop_items(
        category: Optional[str] = None,
        is_featured: Optional[bool] = None
):
    query = {}
    if category:
        query["category"] = category
    if is_featured is not None:
        query["is_featured"] = is_featured
    return await ShopItem.find(query).to_list()


# Single item - public
@router.get("/items/{item_id}", response_model=ShopItem)
async def get_shop_item(item_id: str):
    item = await ShopItem.get(PydanticObjectId(item_id))
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Create item - admin only
@router.post("/items", response_model=ShopItem, status_code=201)
async def create_shop_item(
        item: ShopItem,
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    await item.insert()
    return item


# Seed default items - admin only
@router.post("/items/seed-default")
async def seed_default_items(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    default_items = [
        ShopItem(
            title="Study Shield Premium",
            description="Unlock all premium features of Study Shield",
            price=100,
            image_url="https://images.unsplash.com/photo-1434030216411-0b793f4b4173",
            category="premium",
            is_featured=True
        ),
    ]
    await ShopItem.insert_many(default_items)
    return {"message": "Default shop items seeded"}