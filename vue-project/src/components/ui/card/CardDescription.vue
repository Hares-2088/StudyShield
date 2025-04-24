<!-- src/components/ui/card/CardDescription.vue -->
<template>
    <p class="text-sm text-muted-foreground" :class="className">
      <slot />
    </p>
  </template>
  
  <script setup lang="ts">
  defineProps<{
    className?: string;
  }>();
  </script>