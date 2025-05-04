<template>
  <div class="w-full p-0 md:p-6">
    <h1 class="text-xl md:text-2xl font-bold text-pink-700 mb-4 md:mb-6">Hello, {{ user?.name }}! 🌸</h1>

    <CoinsDisplay />
    <!-- <BlockedWebsites /> -->
    <!-- <PhoneLock /> -->
    <StudyStats />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useUserStore } from '../stores/userStore';
import BlockedWebsites from '../components/BlockedWebsites.vue';
// import PhoneLock from '../components/PhoneLock.vue';
import StudyStats from '../components/StudyStats.vue';
import CoinsDisplay from '../components/CoinsDisplay.vue';

const userStore = useUserStore();
const user = computed(() => userStore.user);
</script>