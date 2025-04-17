<template>
    <div class="profile-container bg-[#bde0fe] p-6 rounded-lg shadow-lg max-w-3xl mx-auto">
        <h2 class="text-2xl font-bold text-[#cdb4db] mb-4">Profile</h2>
        <div class="space-y-4">
            <div>
                <h3 class="text-lg font-semibold text-[#a2d2ff]">User Information</h3>
                <p><strong>Name:</strong> {{ user?.name }}</p>
                <p><strong>Email:</strong> {{ user?.email }}</p>
            </div>
            <div>
                <h3 class="text-lg font-semibold text-[#a2d2ff]">Purchased Items</h3>
                <ul class="list-disc pl-5">
                    <li v-for="item in purchasedItems" :key="item.id" class="text-[#ffafcc]">
                        {{ item.title }} - {{ item.price }}
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
</script>

<style scoped>
.profile-container {
    margin-top: 50px;
}
</style>
