<template>
    <div class="w-full p-4 md:p-6 max-w-3xl mx-auto text-center">
        <h2 class="text-xl font-semibold mb-4">Session In Progress</h2>
        <div class="text-3xl font-mono mb-2">
            {{ formattedTime }}
        </div>
        <div class="text-sm text-gray-600 mb-6">of {{ plannedDuration }} minutes</div>

        <ul class="space-y-3 mb-6 text-left">
            <li v-for="(task, idx) in tasks" :key="idx" class="flex items-center">
                <input type="checkbox" v-model="task.completed" class="mr-2" />
                <span :class="{ 'line-through text-gray-400': task.completed }">
                    {{ task.name }} ({{ task.duration }}m)
                </span>
            </li>
        </ul>

        <button @click="finishSession"
            class="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors w-full shadow-md">
            Finish Session
        </button>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import studySessionService from '@/api/studySessionService';

const route = useRoute();
const router = useRouter();

interface Task {
    name: string;
    duration: number;
    completed: boolean; // Allow completed to be optional
}

const tasks = ref<Task[]>([]);
const plannedDuration = ref(0);
const elapsedSeconds = ref(0);
let timerHandle: number;

const formattedTime = computed(() => {
    const totalSec = elapsedSeconds.value;
    const minutes = Math.floor(totalSec / 60).toString().padStart(2, '0');
    const seconds = (totalSec % 60).toString().padStart(2, '0');
    return `${minutes}:${seconds}`;
});

const fetchSessionData = async () => {
    try {
        const sessionId = route.params.sessionId as string;
        const session = await studySessionService.getStudySession(sessionId);
        // Ensure tasks have a defined completed status, defaulting to false if undefined
        tasks.value = session.tasks.map(task => ({ ...task, completed: task.completed ?? false }));
        plannedDuration.value = session.plannedDuration;
        timerHandle = window.setInterval(() => {
            elapsedSeconds.value++;
        }, 1000);
    } catch (err) {
        console.error('Error fetching session data:', err);
    }
};

const finishSession = async () => {
    clearInterval(timerHandle);
    const actual = Math.floor(elapsedSeconds.value / 60);
    try {
        await studySessionService.completeStudySession(route.params.sessionId as string, actual, 0);
        router.push('/start-session');
    } catch (err) {
        console.error('Error finishing session:', err);
    }
};

onUnmounted(() => {
    clearInterval(timerHandle);
});

fetchSessionData();
</script>
