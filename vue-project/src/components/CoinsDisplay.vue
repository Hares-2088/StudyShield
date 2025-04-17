<template>
    <div class="bg-pink-50 p-4 md:p-6 rounded-lg shadow-md mb-4 md:mb-6">
        <div class="flex items-center justify-between">
            <h2 class="text-lg md:text-xl font-semibold text-pink-700">Your Coins</h2>
            <div class="flex items-center">
                <span class="text-2xl mr-2">🪙</span>
                <span class="text-xl font-bold text-pink-700">{{ coins }}</span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useUserStore } from '../stores/userStore';

const userStore = useUserStore();
const coins = computed(() => userStore.coins || 0);
</script>
