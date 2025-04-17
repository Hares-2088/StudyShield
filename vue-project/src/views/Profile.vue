<template>
    <div class="profile-container bg-[#bde0fe] p-10 rounded-lg shadow-lg max-w-5xl mx-auto">
        <h2 class="text-3xl font-bold text-[#cdb4db] mb-6">Profile</h2>
        <div class="space-y-8">
            <!-- User Information -->
            <div class="p-6 bg-white rounded-lg shadow-md">
                <h3 class="text-xl font-semibold text-[#a2d2ff] mb-4">User Information</h3>
                <p class="text-lg"><strong>Name:</strong> {{ user?.name }}</p>
                <p class="text-lg"><strong>Email:</strong> {{ user?.email }}</p>
                <p class="text-lg"><strong>Coins:</strong> 🪙 {{ user?.coins }}</p>
                <p class="text-lg"><strong>Day Streak:</strong> {{ user?.dayStreak }} days</p>
                <p class="text-lg"><strong>Longest Streak:</strong> {{ user?.longestStreak }} days</p>
            </div>

            <!-- Purchased Items -->
            <div class="p-6 bg-white rounded-lg shadow-md">
                <h3 class="text-xl font-semibold text-[#a2d2ff] mb-4">Purchased Items</h3>
                <ul class="list-disc pl-6">
                    <li v-for="item in purchasedItems" :key="item.id" class="text-lg text-[#ffafcc]">
                        {{ item.title }} - {{ item.price }}
                    </li>
                </ul>
            </div>

            <!-- Achievements -->
            <div class="p-6 bg-white rounded-lg shadow-md">
                <h3 class="text-xl font-semibold text-[#a2d2ff] mb-4">Achievements</h3>
                <ul class="grid grid-cols-2 gap-6">
                    <li v-for="achievement in achievements" :key="achievement.id"
                        class="bg-gray-50 p-6 rounded-lg shadow-md text-center">
                        <span class="text-3xl">{{ achievement.emoji }}</span>
                        <p class="text-lg font-medium text-gray-700 mt-2">{{ achievement.title }}</p>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useUserStore } from '@/stores/userStore';

const userStore = useUserStore();
const user = computed(() => userStore.user);
const purchasedItems = computed(() => userStore.purchasedItems);
const achievements = computed(() => userStore.achievements); // New achievements data
</script>

<style scoped>
.profile-container {
    margin-top: 50px;
}
</style>
