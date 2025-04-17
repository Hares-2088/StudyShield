export interface ShopItem {
    id: string;
    title: string;
    description?: string;
    price: number;
    imageUrl: string;
    category?: string;
    isFeatured?: boolean;
}
