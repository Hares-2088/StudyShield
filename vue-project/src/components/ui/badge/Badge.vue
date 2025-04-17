<template>
    <div class="inline-flex items-center border rounded-full px-2.5 py-0.5 text-xs font-semibold"
        :class="variantClasses">
        <slot></slot>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
    variant?: 'default' | 'secondary' | 'destructive' | 'outline';
}>();

const variantClasses = computed(() => {
    switch (props.variant) {
        case 'secondary':
            return 'bg-gray-100 text-gray-900';
        case 'destructive':
            return 'bg-red-100 text-red-900 border-red-200';
        case 'outline':
            return 'bg-transparent border-gray-200 text-gray-900';
        default:
            return 'bg-pink-100 text-pink-900 border-pink-200';
    }
});
</script>
