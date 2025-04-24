<!-- src/components/ui/chart/ChartTooltip.vue -->
<template>
  <div v-if="active" class="bg-white p-3 rounded-lg shadow-md border text-sm">
    <p class="font-medium">{{ label && formatTooltipDate(label) }}</p>
    <template v-for="item in payload" :key="item.name">
      <p class="text-sm" :style="{ color: item.color }">
        {{ item.name }}: {{ item.value }}
      </p>
    </template>
  </div>
</template>

<script setup lang="ts">
import { formatTooltipDate } from './chartUtils';

defineProps<{
  active?: boolean;
  payload?: any[];
  label?: string;
}>();
</script>