<template>
    <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
        <div class="h-48 overflow-hidden">
            <img :src="item.image" :alt="item.title"
                class="w-full h-full object-cover transition-transform duration-300 hover:scale-105" />
        </div>
        <div class="p-4">
            <h3 class="text-lg font-semibold text-pink-700">{{ item.title }}</h3>
            <p class="text-sm text-[#6c757d] mt-2">{{ item.description }}</p> <!-- Display description -->
            <div class="flex justify-between items-center mt-3">
                <div class="flex items-center">
                    <span class="text-xl mr-1">🪙</span>
                    <span class="font-bold text-pink-600">{{ item.price }}</span>
                </div>
                <button @click="$emit('purchase', item)"
                    class="bg-pink-500 text-white px-4 py-2 rounded-lg hover:bg-pink-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    :disabled="coins < item.price">
                    {{ coins >= item.price ? 'Buy' : 'Not enough coins' }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

interface ShopItemType {
    id: string;
    title: string;
    image: string;
    price: number;
    description?: string;
}

const props = defineProps<{
    item: ShopItemType;
    coins: number;
}>();

defineEmits<{
    (e: 'purchase', item: ShopItemType): void;
}>();
</script>
