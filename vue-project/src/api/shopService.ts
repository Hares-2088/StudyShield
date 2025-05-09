import apiClient from './apiClient';
import type { ShopItem } from '@/models/ShopItem';

export default {
    async getShopItems(): Promise<ShopItem[]> {
        const response = await apiClient.get('/shop/items');
        return response.data;
    },

    async getShopItemById(itemId: string): Promise<ShopItem> {
        const response = await apiClient.get(`/shop/items/${itemId}`);
        return response.data;
    },

    async createShopItem(item: Partial<ShopItem>): Promise<ShopItem> {
        const response = await apiClient.post('/shop/items', item);
        return response.data;
    },

    async seedDefaultItems(): Promise<void> {
        await apiClient.post('/shop/items/seed-default');
    },
};
