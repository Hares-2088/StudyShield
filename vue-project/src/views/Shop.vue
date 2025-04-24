<template>
    <div class="w-full min-h-screen bg-gradient-to-b from-[#FFC8DD]/10 to-[#A2D2FF]/10 p-4 md:p-8">
        <!-- Header Section -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
            <div class="flex items-center">
                <h1 class="text-2xl md:text-3xl font-bold bg-clip-text">
                    Study Shield Shop 🛍️
                </h1>
            </div>

            <!-- Coin Balance with Glass Effect -->
            <div
                class="flex items-center bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full shadow-lg border border-white/20">
                <span class="text-2xl mr-2">🪙</span>
                <span class="font-bold text-white drop-shadow-md">{{ coins.toLocaleString() }}</span>
            </div>
        </div>

        <!-- Success Notification -->
        <div v-if="purchaseSuccess"
            class="bg-[#BDE0FE]/90 backdrop-blur-sm border-l-4 border-[#A2D2FF] text-[#1a1a1a] p-4 mb-6 rounded-lg shadow-md flex justify-between items-center">
            <div class="flex items-center">
                <span class="text-xl mr-3">🎉</span>
                <p class="font-medium">Item purchased successfully! Enjoy your new item.</p>
            </div>
            <button @click="purchaseSuccess = false" class="text-[#1a1a1a] hover:text-[#FFAFCC] transition-colors">
                <span class="text-2xl">×</span>
            </button>
        </div>

        <!-- Shop Items Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <ShopItem v-for="item in shopItems" :key="item.id" :item="item" :coins="coins" @purchase="purchaseItem"
                class="transition-all hover:scale-[1.02] hover:shadow-xl" />
        </div>

        <!-- Empty State -->
        <div v-if="shopItems.length === 0" class="text-center py-16">
            <div class="inline-block p-6 bg-white/20 backdrop-blur-sm rounded-full mb-4">
                <span class="text-4xl">🛒</span>
            </div>
            <h3 class="text-xl font-bold text-[#FFAFCC] mb-2">Shop is Empty</h3>
            <p class="text-[#A2D2FF] max-w-md mx-auto">No items available right now. Check back later for new study
                goodies!</p>
            <button
                class="mt-4 px-6 py-2 bg-gradient-to-r from-[#FFAFCC] to-[#CDB4DB] text-white rounded-full shadow-md hover:shadow-lg transition-all">
                Notify Me
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '../stores/userStore';
import ShopItem from '../components/ShopItem.vue';
import shopApi from '@/api/shopService';

interface IShopItem {
    id: string;
    title: string;
    description?: string;
    price: number;
    image: string;
    category?: string;
    is_featured?: boolean;
}

const userStore = useUserStore();
const coins = computed(() => userStore.coins);
const purchaseSuccess = ref(false);

const shopItems = ref<IShopItem[]>([]);

onMounted(async () => {
    console.log('Fetching shop items...');
    try {
        const items = await shopApi.getShopItems();
        shopItems.value = items.map(i => ({
            id: i._id,
            title: i.title,
            description: i.description, // Ensure description is included
            price: i.price,
            image: i.image_url, // Ensure this maps correctly to the image property
            category: i.category,
            is_featured: i.is_featured,
        }));
        console.log('Shop items fetched successfully:', shopItems.value);
    } catch (err) {
        console.error('Error fetching shop items:', err);
    }
});

const purchaseItem = async (item: IShopItem) => {
    console.log('Attempting to purchase item:', item);
    try {
        await userStore.purchaseShopItem(item.id);
        console.log('Item purchased successfully:', item);
        purchaseSuccess.value = true;
        setTimeout(() => {
            purchaseSuccess.value = false;
        }, 5000);
    } catch (error) {
        console.error('Failed to purchase item:', error);
    }
};
</script>
