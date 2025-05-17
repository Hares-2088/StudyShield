<template>
  <div class="w-full p-4 md:p-6 max-w-3xl mx-auto">
    <!-- Task Builder & Start Button -->
    <TaskInput @add-task="addTask" />
    <TaskList :tasks="tasks" @remove-task="removeTask" class="mt-6" />

    <button @click="startSession"
      class="mt-8 bg-pink-500 text-white px-6 py-3 rounded-lg hover:bg-pink-600 transition-colors w-full shadow-md"
      :disabled="!tasks.length">
      Start Study Session
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import TaskInput from '@/components/TaskInput.vue';
import TaskList from '@/components/TaskList.vue';

import type { Task } from '@/models/Task';

const router = useRouter();
const userStore = useUserStore();

const tasks = ref<Task[]>([]);

const addTask = (task: Task) => tasks.value.push(task);
const removeTask = (idx: number) => tasks.value.splice(idx, 1);

const startSession = async () => {
  if (!tasks.value.length) return;

  // de-proxy your reactive array into plain JS objects
  const plainTasks = tasks.value.map(t => ({
    name: t.name,
    duration: t.duration,
    completed: t.completed,
  }));

  try {
    console.log('→ Creating session with:', plainTasks);
    const session = await userStore.createStudySession(plainTasks);
    console.log('🟢 Got new session back:', session);

    if (!session._id) {
      console.error('❌ No _id returned from backend, cannot navigate.');
      return;
    }

    console.log('component: session from store →', session);

    await router.push({
      name: 'ActiveStudySession',
      params: { sessionId: session._id },
    });
  } catch (err) {
    console.error('🔴 Error starting session:', err);
  }
};

</script>
