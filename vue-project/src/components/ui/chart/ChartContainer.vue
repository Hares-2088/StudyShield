<!-- src/components/ui/chart/ChartContainer.vue -->
<template>
    <div class="w-full" :class="className">
      <slot />
    </div>
  </template>
  
  <script setup lang="ts">
  import type { ChartConfig } from './types';
  
  defineProps<{
    config?: ChartConfig;
    className?: string;
  }>();
  </script>