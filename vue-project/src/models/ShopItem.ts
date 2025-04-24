export interface ShopItem {
    id: string;
    title: string;
    description?: string;
    price: number;
    image_url: string;
    category?: string;
    is_featured?: boolean;
}
