<template>
    <div class="bg-white rounded-lg shadow-md overflow-hidden border border-pink-100">
        <div class="p-4">
            <div class="flex justify-between items-start">
                <h3 class="text-lg font-semibold text-pink-700">{{ challenge.title }}</h3>
                <div class="flex items-center">
                    <span class="text-xl mr-1">🪙</span>
                    <span class="font-bold text-pink-600">
                        {{ displayCoinValue }}
                    </span>
                </div>
            </div>

            <p class="text-sm text-gray-600 mt-2">{{ challenge.description }}</p>

            <!-- Progress bar for challenges with progress tracking -->
            <div v-if="challenge.goal > 1" class="mt-3">
                <div class="flex justify-between text-xs text-pink-600 mb-1">
                    <span>Progress: {{ challenge.progress }} / {{ challenge.goal }}</span>
                    <span>{{ Math.floor((challenge.progress / challenge.goal) * 100) }}%</span>
                </div>
                <Progress :value="(challenge.progress / challenge.goal) * 100" />
            </div>

            <!-- Limited time indicator for special challenges -->
            <div v-if="challenge.limited" class="mt-3 flex items-center text-xs text-orange-600">
                <span class="mr-1">⏱️</span>
                <span>Limited: Expires in {{ challenge.expiresIn }}</span>
            </div>

            <button @click="$emit('complete', challenge.id)"
                class="mt-4 w-full py-2 px-4 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="challenge.isCompleted || challenge.progress < challenge.goal">
                <template v-if="challenge.isCompleted">
                    Completed ✓
                </template>
                <template v-else-if="challenge.progress < challenge.goal">
                    In Progress
                </template>
                <template v-else>
                    Complete
                </template>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import Progress from './ui/progress/Progress.vue';

const props = defineProps({
    challenge: {
        type: Object,
        required: true
    },
    coinMultiplier: {
        type: Number,
        default: 1
    }
});

defineEmits(['complete']);

// Calculate coin value with bonus if applicable
const displayCoinValue = computed(() => {
    if (props.coinMultiplier > 1) {
        return `${props.challenge.coins} x${props.coinMultiplier}`;
    }
    return props.challenge.coins;
});
</script>
