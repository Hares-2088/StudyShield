<!-- components/TaskInput.vue -->
<template>
    <div
        class="bg-gradient-to-br from-[#cdb4db] via-[#ffc8dd] to-[#a2d2ff] opacity-70 animate-gradient p-4 md:p-6 rounded-lg shadow-md mb-6">
        <h2 class="text-lg md:text-xl font-semibold text-pink-700 mb-4">Add a Task</h2>
        <div class="space-y-4">
            <div>
                <label for="taskName" class="block text-sm font-medium text-gray-700">Task Name</label>
                <input id="taskName" v-model="taskName" type="text" placeholder="What are you working on?"
                    class="w-full p-2 border border-[#ffc8dd] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#ffafcc]"
                    @keyup.enter="submitTask" />
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">Time (minutes)</label>
                <div class="flex flex-wrap gap-2">
                    <button @click="setTaskTime(15)"
                        class="bg-white px-4 py-2 rounded-lg hover:bg-[#a2d2ff] transition-colors">
                        15
                    </button>
                    <button @click="setTaskTime(30)"
                        class="bg-white px-4 py-2 rounded-lg hover:bg-[#a2d2ff] transition-colors">
                        30
                    </button>
                    <button @click="setTaskTime(45)"
                        class="bg-white px-4 py-2 rounded-lg hover:bg-[#a2d2ff] transition-colors">
                        45
                    </button>
                    <button @click="setTaskTime(60)"
                        class="bg-white px-4 py-2 rounded-lg hover:bg-[#a2d2ff] transition-colors">
                        60
                    </button>
                </div>
                <input id="taskTime" v-model.number="taskTime" type="number" placeholder="Custom time"
                    class="w-full mt-2 p-2 border border-[#ffc8dd] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#ffafcc]"
                    min="5" step="5" />
            </div>
            <button @click="submitTask"
                class="bg-white px-4 py-2 rounded-lg hover:bg-[#a2d2ff] transition-colors w-full"
                :disabled="!taskName || !taskTime">
                Add Task
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const taskName = ref('');
const taskTime = ref<number>(0); // Initialize with 0
const emit = defineEmits(['add-task']);

const setTaskTime = (time: number) => {
    taskTime.value = (taskTime.value || 0) + time; // Ensure addition as numbers
};

const submitTask = () => {
    if (taskName.value && taskTime.value) {
        emit('add-task', {
            name: taskName.value,
            time: taskTime.value,
            completed: false
        });
        taskName.value = '';
        taskTime.value = 0; // Reset to 0
    }
};
</script>