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
            <div class="flex items-center bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full shadow-lg border border-white/20">
                <span class="text-2xl mr-2">🪙</span>
                <span class="font-bold text-white drop-shadow-md">{{ coins.toLocaleString() }}</span>
            </div>
        </div>

        <!-- Success Notification -->
        <div v-if="purchaseSuccess" class="bg-[#BDE0FE]/90 backdrop-blur-sm border-l-4 border-[#A2D2FF] text-[#1a1a1a] p-4 mb-6 rounded-lg shadow-md flex justify-between items-center">
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
            <ShopItem 
                v-for="item in shopItems" 
                :key="item.id" 
                :item="item" 
                :coins="coins" 
                @purchase="purchaseItem" 
                class="transition-all hover:scale-[1.02] hover:shadow-xl"
            />
        </div>

        <!-- Empty State -->
        <div v-if="shopItems.length === 0" class="text-center py-16">
            <div class="inline-block p-6 bg-white/20 backdrop-blur-sm rounded-full mb-4">
                <span class="text-4xl">🛒</span>
            </div>
            <h3 class="text-xl font-bold text-[#FFAFCC] mb-2">Shop is Empty</h3>
            <p class="text-[#A2D2FF] max-w-md mx-auto">No items available right now. Check back later for new study goodies!</p>
            <button class="mt-4 px-6 py-2 bg-gradient-to-r from-[#FFAFCC] to-[#CDB4DB] text-white rounded-full shadow-md hover:shadow-lg transition-all">
                Notify Me
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useUserStore } from '../stores/userStore';
import ShopItem from '../components/ShopItem.vue';

const userStore = useUserStore();
const coins = computed(() => userStore.coins);
const purchaseSuccess = ref(false);

interface ShopItem {
    id: string;
    title: string;
    image: string;
    price: number;
    description?: string;
}

const shopItems = ref<ShopItem[]>([
    {
        id: '1',
        title: 'Study Shield Premium',
        image: 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80',
        price: 100,
        description: 'Unlock all premium features of Study Shield'
    },
    {
        id: '2',
        title: 'Custom Study Theme',
        image: 'https://images.unsplash.com/photo-1497032628192-86f99bcd76bc?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80',
        price: 50,
        description: 'Personalize your Study Shield experience'
    },
    {
        id: '3',
        title: 'Virtual Study Buddy',
        image: 'https://images.unsplash.com/photo-1581078426770-6d336e5de7bf?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80',
        price: 75,
        description: 'Get a virtual study companion to keep you motivated'
    },
    {
        id: '4',
        title: 'Focus Music Pack',
        image: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80',
        price: 30,
        description: 'Collection of focus-enhancing music tracks'
    },
    {
        id: '5',
        title: 'Digital Productivity Planner',
        image: 'https://images.unsplash.com/photo-1506784983877-45594efa4cbe?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1468&q=80',
        price: 45,
        description: 'Advanced digital planner for optimal productivity'
    },
    {
        id: '6',
        title: 'Study Achievement Badges',
        image: 'https://images.unsplash.com/photo-1533928298208-27ff66555d8d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80',
        price: 25,
        description: 'Unlock exclusive profile badges for study achievements'
    }
]);

const purchaseItem = async (item: ShopItem) => {
    if (coins.value >= item.price) {
        try {
            await userStore.addCoins(-item.price);
            purchaseSuccess.value = true;
            
            setTimeout(() => {
                purchaseSuccess.value = false;
            }, 5000);
        } catch (error) {
            console.error('Failed to purchase item:', error);
        }
    }
};
</script>