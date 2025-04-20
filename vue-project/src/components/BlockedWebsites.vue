<template>
    <div class="bg-white p-4 md:p-6 rounded-lg shadow-md mb-4 md:mb-6">
        <h2 class="text-lg md:text-xl font-semibold text-pink-700 mb-3 md:mb-4">Blocked Websites</h2>
        <ul class="space-y-2">
            <li v-for="site in blockedSites" :key="site"
                class="bg-pink-100 p-2 rounded-lg text-pink-700 flex justify-between items-center">
                <span>{{ site }}</span>
                <button @click="removeBlockedSite(site)"
                    class="bg-pink-200 p-2 rounded-full text-pink-500 hover:bg-pink-300 hover:text-pink-700 transition-colors">
                    <i class="fas fa-trash"></i>
                </button>
            </li>
        </ul>
        <div class="mt-4 flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-2">
            <input v-model="newSite" placeholder="Add a website to block"
                class="w-full p-2 border border-pink-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 text-black" />
            <button @click="addBlockedSite"
                class="bg-pink-500 text-white p-2 rounded-lg hover:bg-pink-600 transition-colors w-full md:w-auto">
                Add
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useUserStore } from '../stores/userStore';

const userStore = useUserStore();
const newSite = ref('');
const blockedSites = computed(() => userStore.blockedSites);

const addBlockedSite = async () => {
    if (newSite.value) {
        await userStore.addBlockedSite(newSite.value);
        newSite.value = '';
    }
};

const removeBlockedSite = async (site: string) => {
    await userStore.removeBlockedSite(site);
};
</script>
