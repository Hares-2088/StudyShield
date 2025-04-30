from beanie import Document
from typing import Optional

class ShopItem(Document):
    title: str
    description: Optional[str]
    price: int
    image_url: str
    class Settings:
        name = "shop_items"
