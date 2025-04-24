<template>
  <div
    class="min-h-screen bg-gradient-to-br from-[#a2d2ff] to-[#cdb4db] flex items-center justify-center py-8 px-4 sm:px-6 rounded-lg">
    <div class="w-full max-w-7xl bg-white/90 rounded-lg shadow-lg p-6 space-y-6">
      <!-- Profile Header -->
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold text-[#4a4e69]">Welcome back, {{ user?.name }}!</h1>
          <p class="text-[#6c757d]">Keep up your study streak!</p>
        </div>
        <div class="flex items-center gap-4">
          <div class="bg-white/80 rounded-lg px-4 py-2 shadow-sm flex items-center gap-2">
            <span class="text-lg">🪙</span>
            <span class="font-bold text-[#4a4e69]">{{ user?.coins }}</span>
          </div>
          <div class="bg-white/80 rounded-lg px-4 py-2 shadow-sm flex items-center gap-2">
            <span class="text-lg">🔥</span>
            <span class="font-bold text-[#4a4e69]">{{ user?.dayStreak }} day streak</span>
          </div>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Focus Time Card -->
        <Card class="bg-white/90 backdrop-blur-sm">
          <CardHeader>
            <CardTitle class="text-[#4a4e69]">Total Focus Time</CardTitle>
            <CardDescription>Lifetime achievement</CardDescription>
          </CardHeader>
          <CardContent>
            <div class="flex items-end gap-2">
              <span class="text-4xl font-bold text-[#4a4e69]">{{ Math.floor((user?.totalFocusTime || 0) / 60) }}</span>
              <span class="text-lg text-muted-foreground mb-1 text-black">hours</span>
            </div>
          </CardContent>
        </Card>

        <!-- Weekly Focus -->
        <Card class="bg-white/90 backdrop-blur-sm">
          <CardHeader>
            <CardTitle class="text-[#4a4e69]">Weekly Focus</CardTitle>
            <CardDescription>This week's progress</CardDescription>
          </CardHeader>
          <CardContent>
            <div class="flex items-end gap-2">
              <span class="text-4xl font-bold text-[#4a4e69]">{{ Math.floor((user?.weeklyFocusTime || 0) / 60) }}</span>
              <span class="text-lg text-muted-foreground mb-1 text-black">hours</span>
            </div>
          </CardContent>
        </Card>

        <!-- Monthly Focus -->
        <Card class="bg-white/90 backdrop-blur-sm">
          <CardHeader>
            <CardTitle class="text-[#4a4e69]">Monthly Focus</CardTitle>
            <CardDescription>This month's progress</CardDescription>
          </CardHeader>
          <CardContent>
            <div class="flex items-end gap-2">
              <span class="text-4xl font-bold text-[#4a4e69]">{{ Math.floor((user?.monthlyFocusTime || 0) / 60)
              }}</span>
              <span class="text-lg text-muted-foreground mb-1 text-black">hours</span>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Focus Time Chart -->
        <Card class="bg-white/90 backdrop-blur-sm">
          <CardHeader>
            <CardTitle>Daily Focus Time</CardTitle>
            <CardDescription>Last 30 days</CardDescription>
          </CardHeader>
          <CardContent class="h-[300px]">
            <canvas ref="barCanvas" class="w-full h-full"></canvas>
          </CardContent>
        </Card>

        <!-- Study Sessions Chart -->
        <Card class="bg-white/90 backdrop-blur-sm">
          <CardHeader>
            <CardTitle>Study Sessions</CardTitle>
            <CardDescription>Sessions vs distractions blocked</CardDescription>
          </CardHeader>
          <CardContent class="h-[300px]">
            <canvas ref="lineCanvas" class="w-full h-full"></canvas>
          </CardContent>
        </Card>
      </div>

      <!-- Rewards and Milestones Section -->

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card class="bg-white/90 backdrop-blur-sm lg:col-span-1">
          <CardHeader>
            <CardTitle class="text-[#4a4e69]">Your Rewards</CardTitle>
            <CardDescription>Items you've unlocked</CardDescription>
          </CardHeader>
          <CardContent>
            <div class="space-y-4">
              <div v-for="item in purchasedItems" :key="item._id"
                class="flex items-center gap-4 p-3 rounded-lg bg-gradient-to-r from-[#ffc8dd]/20 to-[#ffafcc]/20">
                <div class="flex-shrink-0 w-10 h-10 rounded-full bg-[#cdb4db] flex items-center justify-center">
                  <span class="text-white">🪙</span>
                </div>
                <div class="flex-1">
                  <h3 class="font-medium text-[#4a4e69]">{{ item.title }}</h3>
                  <p class="text-sm text-muted-foreground text-black">{{ item.description }}</p>
                </div>
              </div>
              <div v-if="purchasedItems.length === 0" class="text-center py-6 text-muted-foreground">
                No rewards yet. Keep studying to unlock items!
              </div>
            </div>
          </CardContent>
        </Card>

        <Card class="bg-white/90 backdrop-blur-sm lg:col-span-2">
          <CardHeader>
            <CardTitle class="text-[#4a4e69]">Your Milestones</CardTitle>
            <CardDescription>Progress toward your goals</CardDescription>
          </CardHeader>
          <CardContent>
            <div class="space-y-6">
              <div v-for="milestone in milestones" :key="milestone._id" class="space-y-2">
                <div class="flex justify-between items-center">
                  <h3 class="font-medium text-[#4a4e69]">{{ getMilestoneTitle(milestone._id) }}</h3>
                  <span class="text-sm font-medium text-[#6a4c93]">
                    {{ milestone.progress }} / {{ milestone.next_goal }} {{ getMilestoneUnit(milestone._id) }}
                  </span>
                </div>
                + <Progress :value="(milestone.progress / (milestone.next_goal ?? 1)) * 100" class="h-2"
                  :class="getMilestoneColorClass(milestone.current_tier)" />
                <div class="flex justify-between text-xs text-muted-foreground">
                  <span>{{ getTierName(milestone.current_tier) }}</span>
                  <span>{{ getNextTierName(milestone.current_tier) }}</span>
                </div>
              </div>
              <div v-if="milestones.length === 0" class="text-center py-6 text-muted-foreground text-black">
                No active milestones. Complete challenges to unlock!
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { useUserStore } from '@/stores/userStore';
import type { StudyStat } from '@/models/User';

import {
  Chart,
  BarController,
  LineController,
  BarElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip as ChartTooltip,
  Legend,
} from 'chart.js';

// 1) register everything Chart.js needs
Chart.register(
  BarController,
  LineController,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  ChartTooltip,
  Legend
);

// 2) import your card bits so Vue can actually resolve them
import Card from '@/components/ui/card/Card.vue';
import CardHeader from '@/components/ui/card/CardHeader.vue';
import CardTitle from '@/components/ui/card/CardTitle.vue';
import CardDescription from '@/components/ui/card/CardDescription.vue';
import CardContent from '@/components/ui/card/CardContent.vue';

// Progress bar component
import Progress from '@/components/ui/progress/Progress.vue';

// 1️⃣ store + user
const userStore = useUserStore();
const user = computed(() => userStore.user);


// 2️⃣ rewards & milestones
const purchasedItems = computed(() => {
  console.log('Purchased Items:', userStore.purchasedItems); // Debugging output
  return userStore.purchasedItems;
});
const milestones = computed(() => userStore.milestones);

// 3️⃣ chart data (unchanged)
const rawStats = computed<StudyStat[]>(() => userStore.studyStats || []);
const mappedStats = computed(() => {
  const groupedStats: Record<string, { date: string; focus: number; sessions: number; distractions: number }> = {};

  rawStats.value.forEach(s => {
    const dateKey = new Date(s.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    if (!groupedStats[dateKey]) {
      groupedStats[dateKey] = { date: dateKey, focus: 0, sessions: 0, distractions: 0 };
    }
    groupedStats[dateKey].focus += s.focus_time;
    groupedStats[dateKey].sessions += s.sessions;
    groupedStats[dateKey].distractions += s.distractions_blocked;
  });

  return Object.values(groupedStats);
});

// 4) reactive labels + datasets
const labels = computed(() => mappedStats.value.map(s => s.date));
const focusData = computed(() => mappedStats.value.map(s => s.focus));
const sessionData = computed(() => mappedStats.value.map(s => s.sessions));
const distractionData = computed(() => mappedStats.value.map(s => s.distractions));

// 5) canvas refs
const barCanvas = ref<HTMLCanvasElement | null>(null);
const lineCanvas = ref<HTMLCanvasElement | null>(null);

// 6) keep references so we can destroy old charts before re-creating
let barChartInstance: Chart<'bar'> | null = null;
let lineChartInstance: Chart<'line'> | null = null;

// 7) watch your mappedStats and rebuild whenever it changes
const initializeCharts = () => {
  if (mappedStats.value.length && barCanvas.value) {
    // destroy old
    barChartInstance?.destroy();
    barChartInstance = new Chart(barCanvas.value, {
      type: 'bar',
      data: {
        labels: labels.value,
        datasets: [
          {
            label: 'Focus Time (min)',
            data: focusData.value,
            backgroundColor: 'rgba(106,76,147,0.6)',
            borderRadius: 4,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, border: { display: false } },
          y: { grid: { display: false }, border: { display: false } },
        },
      },
    });
  }

  if (mappedStats.value.length && lineCanvas.value) {
    lineChartInstance?.destroy();
    lineChartInstance = new Chart(lineCanvas.value, {
      type: 'line',
      data: {
        labels: labels.value,
        datasets: [
          {
            label: 'Sessions',
            data: sessionData.value,
            borderColor: 'rgba(255,175,204,0.8)',
            pointRadius: 4,
            tension: 0.4,
            fill: false,
          },
          {
            label: 'Distractions Blocked',
            data: distractionData.value,
            borderColor: 'rgba(189,224,254,0.8)',
            pointRadius: 4,
            tension: 0.4,
            fill: false,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'bottom' } },
        scales: {
          x: { grid: { display: false }, border: { display: false } },
          y: { grid: { display: false }, border: { display: false } },
        },
      },
    });
  }
};

watch(mappedStats, initializeCharts, { immediate: true });

// Ensure charts are initialized when the component is mounted
onMounted(() => {
  initializeCharts();
});

// 4️⃣ helper functions for milestones UI
const getMilestoneTitle = (id: string) => {
  const titles: Record<string, string> = {
    'total_focus': 'Total Focus Time',
    'weekly_streak': 'Weekly Streak',
    'distractions_blocked': 'Distractions Blocked',
  };
  return titles[id] || id;
};

const getMilestoneUnit = (id: string) => {
  const units: Record<string, string> = {
    'total_focus': 'hours',
    'weekly_streak': 'days',
    'distractions_blocked': 'blocks',
  };
  return units[id] || '';
};

const getMilestoneColorClass = (tier?: string) => {
  const colors: Record<string, string> = {
    bronze: 'bg-[#cd7f32]',
    silver: 'bg-[#c0c0c0]',
    gold: 'bg-[#ffd700]',
    platinum: 'bg-[#e5e4e2]',
  };
  return colors[tier ?? 'bronze'];
};

const getTierName = (tier?: string) => {
  if (!tier) return 'Start';
  return tier.charAt(0).toUpperCase() + tier.slice(1);
};

const getNextTierName = (currentTier?: string) => {
  const tiers = ['bronze', 'silver', 'gold', 'platinum'];
  if (!currentTier) return 'Bronze';
  const i = tiers.indexOf(currentTier);
  return i < 0 || i === tiers.length - 1
    ? 'Max'
    : tiers[i + 1].charAt(0).toUpperCase() + tiers[i + 1].slice(1);
};
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