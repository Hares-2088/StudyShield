<template>
  <div class="w-full p-4 md:p-6 max-w-3xl mx-auto">
    <!-- Task Builder & Start Button -->
    <div v-if="!activeSession">
      <TaskInput @add-task="addTask" />
      <TaskList :tasks="tasks" @remove-task="removeTask" class="mt-6" />

      <button
        @click="startSession"
        class="mt-8 bg-pink-500 text-white px-6 py-3 rounded-lg hover:bg-pink-600 transition-colors w-full shadow-md"
        :disabled="tasks.length === 0"
      >
        Start Study Session
      </button>
    </div>

    <!-- Active Session Timer & Controls -->
    <div v-else class="text-center">
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

      <button
        @click="finishSession"
        class="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors w-full shadow-md"
      >
        Finish Session
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/userStore';
import TaskInput from '@/components/TaskInput.vue';
import TaskList from '@/components/TaskList.vue';
import studySessionService from '@/api/studySessionService';
import type { Task } from '@/models/Task';

const router = useRouter();
const userStore = useUserStore();

// Tasks before session starts
const tasks = ref<Task[]>([]);

// Active session state
const activeSession = ref<{ id: string; startTime: number } | null>(null);
const plannedDuration = ref<number>(0); // in minutes
const elapsedSeconds = ref<number>(0);
let timerHandle: number;

// Computed formatted time mm:ss
const formattedTime = computed(() => {
  const totalSec = elapsedSeconds.value;
  const minutes = Math.floor(totalSec / 60).toString().padStart(2, '0');
  const seconds = (totalSec % 60).toString().padStart(2, '0');
  return `${minutes}:${seconds}`;
});

// Add and remove tasks
const addTask = (task: { name: string; duration: number }) => {
  tasks.value.push({ ...task, completed: false });
};
const removeTask = (index: number) => tasks.value.splice(index, 1);

// Start session: create on backend, compute duration, start timer
const startSession = async () => {
  plannedDuration.value = tasks.value.reduce((sum, t) => sum + t.duration, 0);
  try {
    const session = await studySessionService.createStudySession(
      userStore.user!.id,
      tasks.value,
      plannedDuration.value
    );
    // initialize timer
    activeSession.value = { id: session._id, startTime: Date.now() };
    elapsedSeconds.value = 0;
    timerHandle = window.setInterval(() => {
      elapsedSeconds.value++;
    }, 1000);
  } catch (err) {
    console.error('Error starting session:', err);
  }
};

// Finish session: stop timer, call backend complete, redirect
const finishSession = async () => {
  if (!activeSession.value) return;
  clearInterval(timerHandle);
  const actual = Math.floor(elapsedSeconds.value / 60);
  const distractions = 0; // optionally track
  try {
    await studySessionService.completeStudySession(
      activeSession.value.id,
      actual,
      distractions
    );
    // navigate to a new session
    router.push('/start-session');
  } catch (err) {
    console.error('Error finishing session:', err);
  }
};

// Clean up timer on unmount
onUnmounted(() => {
  clearInterval(timerHandle);
});
</script>
