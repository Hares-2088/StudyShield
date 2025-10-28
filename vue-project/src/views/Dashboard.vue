<template>
  <div class="w-full p-0 md:p-6">
    <h1 class="text-xl md:text-2xl font-bold text-pink-700 mb-4 md:mb-6">Hello, {{ user?.name }}! 🌸</h1>

    <CoinsDisplay />
    <StudyStats />

    <!-- Active Session Popup -->
    <ActiveSessionPopup :show="showActiveSessionPopup" :session="activeSession" @close="showActiveSessionPopup = false"
      @resume="onResumeSession" @complete="onCompleteSession" />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';
import { useUserStore } from '../stores/userStore';
import StudyStats from '../components/StudyStats.vue';
import CoinsDisplay from '../components/CoinsDisplay.vue';
import ActiveSessionPopup from '../components/ActiveSessionPopup.vue';
import type { StudySession } from '@/models/StudySession';

const userStore = useUserStore();
const user = computed(() => userStore.user);

// Active session popup state
const showActiveSessionPopup = ref(false);
const activeSession = ref<StudySession | null>(null);

// Check for active session when component mounts
onMounted(async () => {
  if (userStore.currentSession) {
    activeSession.value = userStore.currentSession;
    showActiveSessionPopup.value = true;
  }
});

const onResumeSession = (session: StudySession) => {
  console.log('Resuming session:', session);
  // Navigation is handled by the popup component
};

const onCompleteSession = (session: StudySession) => {
  console.log('Completed session:', session);
  // Reset the current session
  userStore.currentSession = null;
  activeSession.value = null;
};
</script>