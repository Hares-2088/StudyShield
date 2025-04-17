<template>
    <div class="relative w-full h-2 bg-gray-200 rounded-full overflow-hidden">
        <div class="h-full transition-all" :style="{ width: `${value}%` }" :class="$attrs.class || 'bg-pink-500'"></div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    value: number;
}>();
</script>
