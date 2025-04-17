from beanie import Document
from typing import Optional


class ShopItem(Document):
    title: str
    description: Optional[str]
    price: int
    image_url: str
    category: Optional[str]
    is_featured: bool = False

    class Settings:
        name = "shop_items"