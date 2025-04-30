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
            <div @click="showNewItemModal = true"
                class="flex justify-center items-center bg-white/20 backdrop-blur-sm rounded-lg shadow-md cursor-pointer hover:shadow-lg transition-all">
                <span class="text-4xl text-[#A2D2FF]">+</span>
            </div>
        </div>

        <!-- New Item Modal -->
        <div v-if="showNewItemModal"
            class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50">
            <div
                class="bg-white/90 backdrop-blur-lg p-6 rounded-2xl shadow-2xl w-full max-w-md border border-[#cdb4db]">
                <h2 class="text-2xl font-bold text-[#4a4e69] mb-6">
                    Add New Shop Item
                </h2>

                <form @submit.prevent="addNewItem" class="space-y-5">
                    <div>
                        <label class="block text-[#4a4e69] font-medium mb-1">Title</label>
                        <input v-model="newItem.title" type="text" required
                            class="w-full p-3 border border-[#a2d2ff] rounded-lg bg-white/80 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-[#ffafcc] text-gray-700" />
                    </div>

                    <div>
                        <label class="block text-[#4a4e69] font-medium mb-1">Description</label>
                        <textarea v-model="newItem.description"
                            class="w-full p-3 border border-[#a2d2ff] rounded-lg bg-white/80 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-[#ffafcc] text-gray-700"></textarea>
                    </div>

                    <div>
                        <label class="block text-[#4a4e69] font-medium mb-1">Price</label>
                        <input v-model.number="newItem.price" type="number" required
                            class="w-full p-3 border border-[#a2d2ff] rounded-lg bg-white/80 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-[#ffafcc] text-gray-700" />
                    </div>

                    <div>
                        <label class="block text-[#4a4e69] font-medium mb-1">Image URL</label>
                        <input v-model="newItem.image_url" type="url" required
                            class="w-full p-3 border border-[#a2d2ff] rounded-lg bg-white/80 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-[#ffafcc] text-gray-700" />
                    </div>

                    <div class="flex justify-end space-x-3 mt-4">
                        <button type="button" @click="showNewItemModal = false"
                            class="px-4 py-2 bg-[#ffc8dd]/60 hover:bg-[#ffc8dd]/80 text-[#4a4e69] rounded-lg transition">
                            Cancel
                        </button>
                        <button type="submit"
                            class="px-4 py-2 bg-gradient-to-r from-[#ffc8dd] to-[#cdb4db] hover:from-[#ffc8dd]/90 hover:to-[#cdb4db]/90 text-white rounded-lg shadow-md transition">
                            Add
                        </button>
                    </div>
                </form>
            </div>
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
}

const userStore = useUserStore();
const coins = computed(() => userStore.coins);
const purchaseSuccess = ref(false);

const shopItems = ref<IShopItem[]>([]);
const showNewItemModal = ref(false);
const newItem = ref({
    title: '',
    description: '',
    price: 0,
    image_url: '',
});

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
    } catch (error: any) {
        console.error('Failed to purchase item:', error);
    }
};

const addNewItem = async () => {
    try {
        await shopApi.createShopItem(newItem.value);
        showNewItemModal.value = false;
        newItem.value = { title: '', description: '', price: 0, image_url: ''};
        const items = await shopApi.getShopItems();
        shopItems.value = items.map(i => ({
            id: i._id,
            title: i.title,
            description: i.description,
            price: i.price,
            image: i.image_url,
        }));
    } catch (error: any) {
        console.error('Failed to add new item:', error);
        console.error('Status:', error.response?.status);
        console.error('Validation errors:', error.response?.data);
    }
};
</script>
