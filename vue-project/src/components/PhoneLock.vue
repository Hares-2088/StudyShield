<template>
    <div class="bg-white p-4 md:p-6 rounded-lg shadow-md mb-4 md:mb-6">
        <h2 class="text-lg md:text-xl font-semibold text-pink-700 mb-3 md:mb-4">Phone Lock</h2>
        <!-- <button @click="togglePhoneLock"
            class="bg-pink-500 text-white p-2 rounded-lg hover:bg-pink-600 transition-colors w-full md:w-auto">
            {{ isPhoneLockEnabled ? 'Disable' : 'Enable' }} Phone Lock
        </button> -->
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useUserStore } from '../stores/userStore';

const userStore = useUserStore();
const isPhoneLockEnabled = computed(() => userStore.isPhoneLockEnabled);

// const togglePhoneLock = async () => {
//     await userStore.togglePhoneLock();
// };
</script>
