<template>
  <div class="w-full p-4 md:p-6 max-w-3xl mx-auto">
    <TaskInput @add-task="addTask" />
    <TaskList 
      :tasks="tasks" 
      @remove-task="removeTask" 
      class="mt-6"
    />
    
    <button
      @click="startSession"
      class="mt-8 bg-pink-500 text-white px-6 py-3 rounded-lg hover:bg-pink-600 transition-colors w-full shadow-md"
      :disabled="tasks.length === 0"
    >
      Start Study Session
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import TaskInput from '@/components/TaskInput.vue';
import TaskList from '@/components/TaskList.vue';

const router = useRouter();
const tasks = ref<{ name: string; duration: number; completed: boolean }[]>([]);

const addTask = (task: { name: string; duration: number }) => {
  tasks.value.push({ ...task, completed: false });
};

const removeTask = (index: number) => {
  tasks.value.splice(index, 1);
};

const startSession = () => {
  // Filter out completed tasks if needed
  const activeTasks = tasks.value.filter(task => !task.completed);
  console.log('Starting session with:', activeTasks);
  // router.push('/study-session'); // Uncomment when you have the route
};
</script>