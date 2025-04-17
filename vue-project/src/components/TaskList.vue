<template>
    <div class="bg-white p-4 md:p-6 rounded-lg shadow-md">
      <div v-if="tasks.length > 0" class="mb-4 flex justify-between items-center">
        <h2 class="text-lg md:text-xl font-semibold text-pink-700">Your Tasks</h2>
        <span class="text-sm text-gray-500">{{ totalTime }} minutes total</span>
      </div>
      
      <ul class="space-y-3">
        <li 
          v-for="(task, index) in tasks" 
          :key="index"
          class="flex justify-between items-center bg-pink-50 p-3 rounded-lg"
        >
          <div class="flex items-center">
            <input 
              type="checkbox" 
              v-model="task.completed"
              class="h-4 w-4 rounded border-pink-300 text-pink-600 focus:ring-pink-500 mr-3"
            >
            <div>
              <h3 class="text-sm font-medium" :class="{ 'line-through text-gray-500': task.completed }">
                {{ task.name }}
              </h3>
              <p class="text-xs text-gray-600">{{ task.duration }} minutes</p>
            </div>
          </div>
          <button 
            @click="$emit('remove-task', index)"
            class="text-pink-500 hover:text-pink-700 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </li>
      </ul>
  
      <div v-if="tasks.length === 0" class="text-center py-4 text-gray-500">
        <p>No tasks added yet</p>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed } from 'vue';
  import type { Task } from '../models/Task';
  
  const props = defineProps({
    tasks: {
      type: Array as () => Task[],
      required: true
    }
  });
  
  const totalTime = computed(() => {
    return props.tasks.reduce((sum, task) => sum + task.duration, 0);
  });
  </script>