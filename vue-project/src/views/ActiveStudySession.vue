<template>
    <div class="w-full p-4 md:p-6 max-w-3xl mx-auto text-center">
        <h2 class="text-xl font-semibold mb-4">Session In Progress</h2>

        <!-- 1) Animated Countdown Ring -->
        <div class="relative w-36 h-36 mx-auto mb-4">
            <svg class="rotate-[-90deg]" viewBox="0 0 100 100">
                <circle class="text-gray-200" cx="50" cy="50" r="45" stroke-width="10" fill="none" />
                <circle class="text-gradient-from-to transition-all duration-500 ease-linear"
                    :stroke-dasharray="circumference"
                    :stroke-dashoffset="circumference - (elapsedSeconds / (plannedDuration * 60)) * circumference"
                    cx="50" cy="50" r="45" stroke-width="10" stroke-linecap="round" fill="none" />
            </svg>
            <!-- 2) Flip-digit timer -->
            <div class="absolute inset-0 flex flex-col items-center justify-center">
                <div class="text-3xl font-mono mb-1 flex space-x-1">
                    <span v-for="(digit, idx) in formattedTime.split('')" :key="idx" class="inline-block flip-digit">{{
                        digit }}</span>
                </div>
                <div class="text-sm text-gray-600">
                    of {{ plannedDuration }} min
                </div>
            </div>
        </div>

        <!-- 3) Progress bar fallback -->
        <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden mb-6">
            <div class="h-full bg-gradient-to-r from-[#FFC8DD] to-[#A2D2FF] transition-all duration-500 ease-linear"
                :style="{ width: `${(elapsedSeconds / (plannedDuration * 60)) * 100}%` }" />
        </div>

        <!-- 4) Task list with animated transitions -->
        <transition-group name="list" tag="ul" class="space-y-3 mb-6 text-left">
            <li v-for="(task, idx) in tasks" :key="task.name"
                class="flex items-center bg-white/20 backdrop-blur-sm p-2 rounded-lg shadow-sm hover:shadow-md transition-shadow">
                <input type="checkbox" v-model="task.completed"
                    class="mr-2 form-checkbox h-5 w-5 text-[#A2D2FF] transition-colors" />
                <span :class="{ 'line-through text-gray-400': task.completed }" class="flex-1 transition-colors">
                    {{ task.name }} <small class="text-xs">({{ task.duration }}m)</small>
                </span>
            </li>
        </transition-group>

        <button @click="finishSession" class="w-full bg-gradient-to-r from-[#A2D2FF] to-[#FFAFCC] text-white py-3 rounded-lg
               hover:from-[#A2D2FF]/90 hover:to-[#FFAFCC]/90 active:scale-95 transition-all shadow-md">
            Finish Session
        </button>

        <!-- 5) Encouragement Modal with fade/scale -->
        <transition name="fade-scale">
            <div v-if="showEncouragement"
                class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div class="bg-white p-6 rounded-2xl shadow-2xl text-center max-w-sm transform transition-transform">
                    <img :src="randomImage" alt="Encouragement" class="w-32 h-32 mx-auto mb-4" />
                    <p class="text-lg  text-[#FFAFCC] font-semibold mb-4">{{ randomMessage }}</p>
                    <button @click="closeEncouragement"
                        class="bg-[#A2D2FF] text-black px-4 py-2 rounded-lg hover:bg-[#A2D2FF]/90 transition-colors">
                        Continue
                    </button>
                </div>
            </div>
        </transition>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import studySessionService from '@/api/studySessionService';

interface Task { name: string; duration: number; completed: boolean; }

const route = useRoute();
const router = useRouter();

const tasks = ref<Task[]>([]);
const plannedDuration = ref(0);
const elapsedSeconds = ref(0);
let timerHandle: number;

// For the SVG ring
const circumference = 2 * Math.PI * 45; // 2πr, with r=45

// Encouragement
const showEncouragement = ref(false);
const randomMessage = ref('');
const randomImage = ref('');
const encouragementMessages = [
    "Great job! Keep up the good work!",
    "You're doing amazing! Stay focused!",
    "Fantastic effort! Keep pushing forward!",
    "Well done! You're making progress!"
];
const catStickerImages = [
    '/catStickers/cat.png',
    '/catStickers/communications.png',
    '/catStickers/grade.png',
    '/catStickers/reading.png',
    '/catStickers/weights.png',
];

const formattedTime = computed(() => {
    const m = Math.floor(elapsedSeconds.value / 60).toString().padStart(2, '0');
    const s = (elapsedSeconds.value % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
});

async function fetchSessionData() {
    try {
        const id = route.params.sessionId as string;
        const session = await studySessionService.getStudySession(id);
        tasks.value = session.tasks.map(t => ({ ...t, completed: !!t.completed }));
        plannedDuration.value = session.plannedDuration; // <-- This is where plannedDuration is set
        timerHandle = window.setInterval(() => elapsedSeconds.value++, 1000);
    } catch (e) {
        console.error(e);
    }
}

async function finishSession() {
    clearInterval(timerHandle);
    const actualMins = Math.floor(elapsedSeconds.value / 60);
    try {
        await studySessionService.completeStudySession(route.params.sessionId as string, actualMins, 0);
        randomMessage.value = encouragementMessages[Math.floor(Math.random() * encouragementMessages.length)];
        randomImage.value = catStickerImages[Math.floor(Math.random() * catStickerImages.length)];
        showEncouragement.value = true;
    } catch (e) { console.error(e); }
}

function closeEncouragement() {
    showEncouragement.value = false;
    router.push('/start-session');
}

onUnmounted(() => clearInterval(timerHandle));
fetchSessionData();
</script>

<style scoped>
/* flip every digit when it changes */
.flip-digit {
    display: inline-block;
    transition: transform 0.3s ease;
}

.flip-digit::before {
    content: attr(data-old);
    position: absolute;
    transform-origin: bottom;
    transform: rotateX(90deg);
    backface-visibility: hidden;
}

/* list enter/leave */
.list-enter-from,
.list-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

.list-enter-active,
.list-leave-active {
    transition: all 0.3s ease;
}

/* fade + scale modal */
.fade-scale-enter-from {
    opacity: 0;
    transform: scale(0.9);
}

.fade-scale-enter-active {
    transition: all 0.25s ease-out;
}

.fade-scale-leave-to {
    opacity: 0;
    transform: scale(0.9);
}

.fade-scale-leave-active {
    transition: all 0.2s ease-in;
}

/* gradient stroke color binding */
.text-gradient-from-to {
    stroke: url(#gradient);
    /* or simply use `stroke="#A2D2FF"` */
}
</style>
