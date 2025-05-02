<template>
  <div class="w-full p-4 md:p-6 max-w-3xl mx-auto">
    <!-- Task Builder & Start Button -->
    <TaskInput @add-task="addTask" />
    <TaskList :tasks="tasks" @remove-task="removeTask" class="mt-6" />

    <button @click="startSession"
      class="mt-8 bg-pink-500 text-white px-6 py-3 rounded-lg hover:bg-pink-600 transition-colors w-full shadow-md"
      :disabled="tasks.length === 0">
      Start Study Session
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/userStore';
import TaskInput from '@/components/TaskInput.vue';
import TaskList from '@/components/TaskList.vue';
import studySessionService from '@/api/studySessionService';
import type { Task } from '@/models/Task';

const router = useRouter();
const userStore = useUserStore();

const tasks = ref<Task[]>([]);

const addTask = (task: { name: string; duration: number }) => {
  tasks.value.push({ ...task, completed: false });
};
const removeTask = (index: number) => tasks.value.splice(index, 1);

const startSession = async () => {
  const plannedDuration = tasks.value.reduce((sum, t) => sum + t.duration, 0);
  try {
    const session = await studySessionService.createStudySession(
      userStore.user!.id,
      tasks.value,
      plannedDuration
    );
    router.push({ name: 'ActiveStudySession', params: { sessionId: session._id } });
  } catch (err) {
    console.error('Error starting session:', err);
  }
};
</script>
