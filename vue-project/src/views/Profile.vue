<template>
  <div class="bg-gradient-to-r from-[#bde0fe] to-[#cdb4db] min-h-screen py-12 px-4">
    <div class="max-w-7xl mx-auto">
      <h2 class="text-4xl font-bold text-[#4a4e69] mb-8">User Profile</h2>

      <div class="grid md:grid-cols-3 gap-8">
        <!-- User Information -->
        <div class="bg-white shadow-lg rounded-xl p-8 md:col-span-1">
          <h3 class="text-2xl font-semibold text-[#6a4c93] mb-4">User Information</h3>
          <div class="space-y-3">
            <p class="text-gray-700"><span class="font-semibold">Name:</span> {{ user?.name }}</p>
            <p class="text-gray-700"><span class="font-semibold">Email:</span> {{ user?.email }}</p>
            <p class="text-gray-700"><span class="font-semibold">Coins:</span> 🪙 {{ user?.coins }}</p>
            <p class="text-gray-700"><span class="font-semibold">Day Streak:</span> {{ user?.dayStreak }} days</p>
            <p class="text-gray-700"><span class="font-semibold">Longest Streak:</span> {{ user?.longestStreak }} days
            </p>
          </div>
        </div>

        <!-- Purchased Items -->
        <div class="bg-white shadow-lg rounded-xl p-8 md:col-span-1">
          <h3 class="text-2xl font-semibold text-[#6a4c93] mb-4">Purchased Items</h3>
          <ul class="space-y-2 max-h-72 overflow-auto">
            <li v-for="item in purchasedItems" :key="item.id"
              class="flex justify-between items-center bg-gray-100 rounded-lg px-4 py-2">
              <span>{{ item.title }}</span>
              <span class="text-gray-600">{{ item.price }} 🪙</span>
            </li>
          </ul>
        </div>

        <!-- Milestones -->
        <div class="bg-white shadow-lg rounded-xl p-8 md:col-span-1">
          <h3 class="text-2xl font-semibold text-[#6a4c93] mb-4">Milestones</h3>
          <div class="grid grid-cols-2 gap-4">
            <div v-for="milestone in milestones" :key="milestone._id"
              class="bg-[#f0e6ef] rounded-xl shadow-md p-4 text-center">
              <span class="text-3xl font-bold text-[#4a4e69]">{{ milestone.progress }}</span>
              <p class="text-sm text-gray-600 capitalize mt-1">{{ milestone.current_tier }}</p>
            </div>
          </div>
        </div>
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
const milestones = computed(() => userStore.milestones);
</script>

<style scoped>
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-thumb {
  background-color: #6a4c93;
  border-radius: 10px;
}
</style>