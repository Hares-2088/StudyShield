<template>
  <!-- ... (keep all existing template code until Charts Section) ... -->

  <!-- Charts Section -->
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <!-- Focus Time Chart -->
    <Card class="bg-white/90 backdrop-blur-sm">
      <CardHeader>
        <CardTitle class="text-[#4a4e69]">Daily Focus Time</CardTitle>
        <CardDescription>Last 30 days</CardDescription>
      </CardHeader>
      <CardContent class="h-[300px] relative">
        <div v-if="!focusTimeChartData.length" class="absolute inset-0 flex items-center justify-center">
          <p class="text-muted-foreground">No focus time data available</p>
        </div>
        <div v-else class="w-full h-full">
          <BarChart
            :width="500"
            :height="300"
            :data="focusTimeChartData"
            :margin="{ top: 20, right: 20, left: 20, bottom: 20 }"
          >
            <CartesianGrid strokeDasharray="3 3" :vertical="false" />
            <XAxis 
              dataKey="date"
              :tickFormatter="formatChartDate"
              :tickLine="false"
              :axisLine="false"
            />
            <YAxis 
              :tickLine="false"
              :axisLine="false"
            />
            <Tooltip 
              :formatter="(value: number) => [`${value} minutes`, 'Focus Time']"
              :labelFormatter="formatTooltipDate"
            />
            <Bar 
              dataKey="focusTime" 
              fill="#6a4c93"
              :radius="[4, 4, 0, 0]"
            />
          </BarChart>
        </div>
      </CardContent>
    </Card>

    <!-- Study Sessions Chart -->
    <Card class="bg-white/90 backdrop-blur-sm">
      <CardHeader>
        <CardTitle class="text-[#4a4e69]">Study Sessions</CardTitle>
        <CardDescription>Sessions vs distractions blocked</CardDescription>
      </CardHeader>
      <CardContent class="h-[300px] relative">
        <div v-if="!sessionsChartData.length" class="absolute inset-0 flex items-center justify-center">
          <p class="text-muted-foreground">No session data available</p>
        </div>
        <div v-else class="w-full h-full">
          <LineChart
            :width="500"
            :height="300"
            :data="sessionsChartData"
            :margin="{ top: 20, right: 20, left: 20, bottom: 20 }"
          >
            <CartesianGrid strokeDasharray="3 3" :vertical="false" />
            <XAxis 
              dataKey="date"
              :tickFormatter="formatChartDate"
              :tickLine="false"
              :axisLine="false"
            />
            <YAxis 
              :tickLine="false"
              :axisLine="false"
            />
            <Tooltip 
              :formatter="(value: number, name: string) => [
                value, 
                name === 'sessions' ? 'Sessions' : 'Distractions Blocked'
              ]"
              :labelFormatter="formatTooltipDate"
            />
            <Line
              type="monotone"
              dataKey="sessions"
              stroke="#ffafcc"
              :strokeWidth="2"
              :dot="{ r: 4 }"
            />
            <Line
              type="monotone"
              dataKey="distractionsBlocked"
              stroke="#bde0fe"
              :strokeWidth="2"
              :dot="{ r: 4 }"
            />
          </LineChart>
        </div>
      </CardContent>
    </Card>
  </div>

  <!-- ... (rest of your template remains the same) ... -->
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useUserStore } from '@/stores/userStore';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import {
  BarChart,
  LineChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from 'recharts';

const userStore = useUserStore();

// Use the store's computed properties directly
const user = computed(() => userStore.user);
const purchasedItems = computed(() => userStore.purchasedItems);
const milestones = computed(() => userStore.milestones);
const studyStats = computed(() => userStore.studyStats || []);

// Chart data computations
const focusTimeChartData = computed(() => {
  return studyStats.value.map(stat => ({
    date: stat.date,
    focusTime: stat.focusTime || 0,
  }));
});

const sessionsChartData = computed(() => {
  return studyStats.value.map(stat => ({
    date: stat.date,
    sessions: stat.sessions || 0,
    distractionsBlocked: stat.distractionsBlocked || 0,
  }));
});

// Date formatting with error handling
const formatChartDate = (dateString: string) => {
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  } catch {
    return '';
  }
};

const formatTooltipDate = (dateString: string) => {
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    });
  } catch {
    return '';
  }
};

// ... (keep all your existing helper functions) ...
</script>

<style>
/* Custom chart styles that won't affect other components */
.recharts-wrapper .recharts-cartesian-grid-horizontal line {
  stroke: #f1f5f9;
}

.recharts-wrapper .recharts-cartesian-grid-vertical line {
  stroke: #f1f5f9;
}

.recharts-tooltip-wrapper {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  padding: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.recharts-default-tooltip {
  margin: 0;
  font-family: inherit;
}

.recharts-tooltip-label {
  font-weight: 600;
  color: #4a4e69;
  margin-bottom: 0.25rem;
}

.recharts-tooltip-item {
  color: #64748b;
  margin: 0 !important;
}
</style>