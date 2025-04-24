# last prompt

help me make a better profile page. here is the one i have for now:
<template>
  <div class="bg-gradient-to-r from-[#bde0fe] to-[#cdb4db] min-h-screen py-12 px-4">
    <div class="max-w-7xl mx-auto space-y-8">
      <h2 class="text-4xl font-bold text-[#4a4e69] mb-8">User Profile</h2>

      <!-- User Information -->
      <Card>
        <CardHeader>
          <CardTitle>User Information</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-3">
            <p><span class="font-semibold">Name:</span> {{ user?.name }}</p>
            <p><span class="font-semibold">Email:</span> {{ user?.email }}</p>
            <p><span class="font-semibold">Coins:</span> 🪙 {{ user?.coins }}</p>
            <p><span class="font-semibold">Day Streak:</span> {{ user?.dayStreak }} days</p>
            <p><span class="font-semibold">Longest Streak:</span> {{ user?.longestStreak }} days</p>
          </div>
        </CardContent>
      </Card>

      <!-- Focus Time Chart -->
      <Card>
        <CardHeader>
          <CardTitle>Focus Time Consistency</CardTitle>
        </CardHeader>
        <CardContent>
          <LineChart :data="focusTimeChartData" />
        </CardContent>
      </Card>

      <!-- Purchased Items -->
      <Card>
        <CardHeader>
          <CardTitle>Purchased Items</CardTitle>
        </CardHeader>
        <CardContent>
          <ul class="space-y-2 max-h-72 overflow-auto">
            <li v-for="item in purchasedItems" :key="item._id"
              class="flex justify-between items-center bg-gray-100 rounded-lg px-4 py-2">
              <span>{{ item.title }}</span>
              <span class="text-gray-600">{{ item.price }} 🪙</span>
            </li>
          </ul>
        </CardContent>
      </Card>

      <!-- Study Stats -->
      <Card>
        <CardHeader>
          <CardTitle>Study Statistics</CardTitle>
        </CardHeader>
        <CardContent>
          <BarChart :data="studyStatsChartData" />
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useUserStore } from '@/stores/userStore';
import Card from '@/components/ui/card/Card.vue';
import CardHeader from '@/components/ui/card/CardHeader.vue';
import CardTitle from '@/components/ui/card/CardTitle.vue';
import CardContent from '@/components/ui/card/CardContent.vue';
import LineChart from '@/components/ui/charts/LineChart.vue';
import BarChart from '@/components/ui/charts/BarChart.vue';

const userStore = useUserStore();
const user = computed(() => userStore.user);
const purchasedItems = computed(() => userStore.purchasedItems);

// Prepare data for focus time chart
const focusTimeChartData = computed(() => {
  return {
    labels: userStore.studyStats.map(stat => new Date(stat.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Focus Time (minutes)',
        data: userStore.studyStats.map(stat => stat.focusTime),
        backgroundColor: '#6a4c93',
        borderColor: '#6a4c93',
        fill: false,
      },
    ],
  };
});

// Prepare data for study stats chart
const studyStatsChartData = computed(() => {
  return {
    labels: userStore.studyStats.map(stat => new Date(stat.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Sessions',
        data: userStore.studyStats.map(stat => stat.sessions),
        backgroundColor: '#bde0fe',
      },
      {
        label: 'Distractions Blocked',
        data: userStore.studyStats.map(stat => stat.distractionsBlocked),
        backgroundColor: '#cdb4db',
      },
    ],
  };
});
</script>

<style scoped>
/* Add any additional styling if needed */
</style>

i wish to destroy it and do it all over again because it is really ugly. i also want to add charts. i am using vue and tailwind. the charts i want to use are those from shadcn ui:
"use client"

import * as React from "react"
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
const chartData = [
  { date: "2024-04-01", desktop: 222, mobile: 150 },
  { date: "2024-04-02", desktop: 97, mobile: 180 },
  { date: "2024-04-03", desktop: 167, mobile: 120 },
  { date: "2024-04-04", desktop: 242, mobile: 260 },
  { date: "2024-04-05", desktop: 373, mobile: 290 },
  { date: "2024-04-06", desktop: 301, mobile: 340 },
  { date: "2024-04-07", desktop: 245, mobile: 180 },
  { date: "2024-04-08", desktop: 409, mobile: 320 },
  { date: "2024-04-09", desktop: 59, mobile: 110 },
  { date: "2024-04-10", desktop: 261, mobile: 190 },
  { date: "2024-04-11", desktop: 327, mobile: 350 },
  { date: "2024-04-12", desktop: 292, mobile: 210 },
  { date: "2024-04-13", desktop: 342, mobile: 380 },
  { date: "2024-04-14", desktop: 137, mobile: 220 },
  { date: "2024-04-15", desktop: 120, mobile: 170 },
  { date: "2024-04-16", desktop: 138, mobile: 190 },
  { date: "2024-04-17", desktop: 446, mobile: 360 },
  { date: "2024-04-18", desktop: 364, mobile: 410 },
  { date: "2024-04-19", desktop: 243, mobile: 180 },
  { date: "2024-04-20", desktop: 89, mobile: 150 },
  { date: "2024-04-21", desktop: 137, mobile: 200 },
  { date: "2024-04-22", desktop: 224, mobile: 170 },
  { date: "2024-04-23", desktop: 138, mobile: 230 },
  { date: "2024-04-24", desktop: 387, mobile: 290 },
  { date: "2024-04-25", desktop: 215, mobile: 250 },
  { date: "2024-04-26", desktop: 75, mobile: 130 },
  { date: "2024-04-27", desktop: 383, mobile: 420 },
  { date: "2024-04-28", desktop: 122, mobile: 180 },
  { date: "2024-04-29", desktop: 315, mobile: 240 },
  { date: "2024-04-30", desktop: 454, mobile: 380 },
  { date: "2024-05-01", desktop: 165, mobile: 220 },
  { date: "2024-05-02", desktop: 293, mobile: 310 },
  { date: "2024-05-03", desktop: 247, mobile: 190 },
  { date: "2024-05-04", desktop: 385, mobile: 420 },
  { date: "2024-05-05", desktop: 481, mobile: 390 },
  { date: "2024-05-06", desktop: 498, mobile: 520 },
  { date: "2024-05-07", desktop: 388, mobile: 300 },
  { date: "2024-05-08", desktop: 149, mobile: 210 },
  { date: "2024-05-09", desktop: 227, mobile: 180 },
  { date: "2024-05-10", desktop: 293, mobile: 330 },
  { date: "2024-05-11", desktop: 335, mobile: 270 },
  { date: "2024-05-12", desktop: 197, mobile: 240 },
  { date: "2024-05-13", desktop: 197, mobile: 160 },
  { date: "2024-05-14", desktop: 448, mobile: 490 },
  { date: "2024-05-15", desktop: 473, mobile: 380 },
  { date: "2024-05-16", desktop: 338, mobile: 400 },
  { date: "2024-05-17", desktop: 499, mobile: 420 },
  { date: "2024-05-18", desktop: 315, mobile: 350 },
  { date: "2024-05-19", desktop: 235, mobile: 180 },
  { date: "2024-05-20", desktop: 177, mobile: 230 },
  { date: "2024-05-21", desktop: 82, mobile: 140 },
  { date: "2024-05-22", desktop: 81, mobile: 120 },
  { date: "2024-05-23", desktop: 252, mobile: 290 },
  { date: "2024-05-24", desktop: 294, mobile: 220 },
  { date: "2024-05-25", desktop: 201, mobile: 250 },
  { date: "2024-05-26", desktop: 213, mobile: 170 },
  { date: "2024-05-27", desktop: 420, mobile: 460 },
  { date: "2024-05-28", desktop: 233, mobile: 190 },
  { date: "2024-05-29", desktop: 78, mobile: 130 },
  { date: "2024-05-30", desktop: 340, mobile: 280 },
  { date: "2024-05-31", desktop: 178, mobile: 230 },
  { date: "2024-06-01", desktop: 178, mobile: 200 },
  { date: "2024-06-02", desktop: 470, mobile: 410 },
  { date: "2024-06-03", desktop: 103, mobile: 160 },
  { date: "2024-06-04", desktop: 439, mobile: 380 },
  { date: "2024-06-05", desktop: 88, mobile: 140 },
  { date: "2024-06-06", desktop: 294, mobile: 250 },
  { date: "2024-06-07", desktop: 323, mobile: 370 },
  { date: "2024-06-08", desktop: 385, mobile: 320 },
  { date: "2024-06-09", desktop: 438, mobile: 480 },
  { date: "2024-06-10", desktop: 155, mobile: 200 },
  { date: "2024-06-11", desktop: 92, mobile: 150 },
  { date: "2024-06-12", desktop: 492, mobile: 420 },
  { date: "2024-06-13", desktop: 81, mobile: 130 },
  { date: "2024-06-14", desktop: 426, mobile: 380 },
  { date: "2024-06-15", desktop: 307, mobile: 350 },
  { date: "2024-06-16", desktop: 371, mobile: 310 },
  { date: "2024-06-17", desktop: 475, mobile: 520 },
  { date: "2024-06-18", desktop: 107, mobile: 170 },
  { date: "2024-06-19", desktop: 341, mobile: 290 },
  { date: "2024-06-20", desktop: 408, mobile: 450 },
  { date: "2024-06-21", desktop: 169, mobile: 210 },
  { date: "2024-06-22", desktop: 317, mobile: 270 },
  { date: "2024-06-23", desktop: 480, mobile: 530 },
  { date: "2024-06-24", desktop: 132, mobile: 180 },
  { date: "2024-06-25", desktop: 141, mobile: 190 },
  { date: "2024-06-26", desktop: 434, mobile: 380 },
  { date: "2024-06-27", desktop: 448, mobile: 490 },
  { date: "2024-06-28", desktop: 149, mobile: 200 },
  { date: "2024-06-29", desktop: 103, mobile: 160 },
  { date: "2024-06-30", desktop: 446, mobile: 400 },
]

const chartConfig = {
  views: {
    label: "Page Views",
  },
  desktop: {
    label: "Desktop",
    color: "hsl(var(--chart-1))",
  },
  mobile: {
    label: "Mobile",
    color: "hsl(var(--chart-2))",
  },
} satisfies ChartConfig

export function Component() {
  const [activeChart, setActiveChart] =
    React.useState<keyof typeof chartConfig>("desktop")

  const total = React.useMemo(
    () => ({
      desktop: chartData.reduce((acc, curr) => acc + curr.desktop, 0),
      mobile: chartData.reduce((acc, curr) => acc + curr.mobile, 0),
    }),
    []
  )

  return (
    <Card>
      <CardHeader className="flex flex-col items-stretch space-y-0 border-b p-0 sm:flex-row">
        <div className="flex flex-1 flex-col justify-center gap-1 px-6 py-5 sm:py-6">
          <CardTitle>Bar Chart - Interactive</CardTitle>
          <CardDescription>
            Showing total visitors for the last 3 months
          </CardDescription>
        </div>
        <div className="flex">
          {["desktop", "mobile"].map((key) => {
            const chart = key as keyof typeof chartConfig
            return (
              <button
                key={chart}
                data-active={activeChart === chart}
                className="relative z-30 flex flex-1 flex-col justify-center gap-1 border-t px-6 py-4 text-left even:border-l data-[active=true]:bg-muted/50 sm:border-l sm:border-t-0 sm:px-8 sm:py-6"
                onClick={() => setActiveChart(chart)}
              >
                <span className="text-xs text-muted-foreground">
                  {chartConfig[chart].label}
                </span>
                <span className="text-lg font-bold leading-none sm:text-3xl">
                  {total[key as keyof typeof total].toLocaleString()}
                </span>
              </button>
            )
          })}
        </div>
      </CardHeader>
      <CardContent className="px-2 sm:p-6">
        <ChartContainer
          config={chartConfig}
          className="aspect-auto h-[250px] w-full"
        >
          <BarChart
            accessibilityLayer
            data={chartData}
            margin={{
              left: 12,
              right: 12,
            }}
          >
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="date"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              minTickGap={32}
              tickFormatter={(value) => {
                const date = new Date(value)
                return date.toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                })
              }}
            />
            <ChartTooltip
              content={
                <ChartTooltipContent
                  className="w-[150px]"
                  nameKey="views"
                  labelFormatter={(value) => {
                    return new Date(value).toLocaleDateString("en-US", {
                      month: "short",
                      day: "numeric",
                      year: "numeric",
                    })
                  }}
                />
              }
            />
            <Bar dataKey={activeChart} fill={`var(--color-${activeChart})`} />
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}

"use client"

import { TrendingUp } from "lucide-react"
import { CartesianGrid, Dot, Line, LineChart } from "recharts"

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
const chartData = [
  { browser: "chrome", visitors: 275, fill: "var(--color-chrome)" },
  { browser: "safari", visitors: 200, fill: "var(--color-safari)" },
  { browser: "firefox", visitors: 187, fill: "var(--color-firefox)" },
  { browser: "edge", visitors: 173, fill: "var(--color-edge)" },
  { browser: "other", visitors: 90, fill: "var(--color-other)" },
]

const chartConfig = {
  visitors: {
    label: "Visitors",
    color: "hsl(var(--chart-2))",
  },
  chrome: {
    label: "Chrome",
    color: "hsl(var(--chart-1))",
  },
  safari: {
    label: "Safari",
    color: "hsl(var(--chart-2))",
  },
  firefox: {
    label: "Firefox",
    color: "hsl(var(--chart-3))",
  },
  edge: {
    label: "Edge",
    color: "hsl(var(--chart-4))",
  },
  other: {
    label: "Other",
    color: "hsl(var(--chart-5))",
  },
} satisfies ChartConfig

export function Component() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Line Chart - Dots Colors</CardTitle>
        <CardDescription>January - June 2024</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <LineChart
            accessibilityLayer
            data={chartData}
            margin={{
              top: 24,
              left: 24,
              right: 24,
            }}
          >
            <CartesianGrid vertical={false} />
            <ChartTooltip
              cursor={false}
              content={
                <ChartTooltipContent
                  indicator="line"
                  nameKey="visitors"
                  hideLabel
                />
              }
            />
            <Line
              dataKey="visitors"
              type="natural"
              stroke="var(--color-visitors)"
              strokeWidth={2}
              dot={({ payload, ...props }) => {
                return (
                  <Dot
                    key={payload.browser}
                    r={5}
                    cx={props.cx}
                    cy={props.cy}
                    fill={payload.fill}
                    stroke={payload.fill}
                  />
                )
              }}
            />
          </LineChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col items-start gap-2 text-sm">
        <div className="flex gap-2 font-medium leading-none">
          Trending up by 5.2% this month <TrendingUp className="h-4 w-4" />
        </div>
        <div className="leading-none text-muted-foreground">
          Showing total visitors for the last 6 months
        </div>
      </CardFooter>
    </Card>
  )
}

now fyi my app is about helping the user study and keep track of their study sessions. here are some other components i have that may help you:
import type { ShopItem } from './ShopItem';
import type { TierName } from './Milestone';

export interface ChallengeProgress {
    challenge_id: string; // ID of the challenge
    progress: number;
    is_completed: boolean;
    last_updated: string; // ISO string
}

export interface MilestoneProgress {
    _id: string; // ID of the milestone
    progress: number;
    current_tier?: TierName;
    next_goal?: number;
}

export interface StudyStat {
    date: string; // ISO string
    focusTime: number; // in minutes
    sessions: number;
    distractionsBlocked: number;
}

export interface User {
    id: string;
    name: string;
    email: string;
    coins: number;
    dayStreak: number;
    longestStreak: number;
    lastActiveDate?: string; // ISO string
    challenges: ChallengeProgress[];
    milestones: MilestoneProgress[];
    purchasedItems: ShopItem[];
    blockedWebsites: string[];          // matches the API field
    totalFocusTime: number; // in minutes
    weeklyFocusTime: number;
    monthlyFocusTime: number;
    studyStats: StudyStat[];
    isPhoneLockEnabled: boolean;
    isActive?: boolean; // Optional, for admin functionality
    role?: 'user' | 'admin'; // Optional, for role-based functionality
    lastLogin?: string; // ISO string, optional
}


export interface Task {
  name: string;
  duration: number; // in minutes
  completed?: boolean;
}
import type { Task } from './Task';

export interface StudySession {
    _id: string;
    userId: string;
    tasks: Task[];
    plannedDuration: number; // in minutes
    actual_duration?: number; // in minutes
    startTime: string; // ISO string
    endTime?: string; // ISO string
    distractionsBlocked: number;
    notes?: string;
}

export enum TierName {
    BRONZE = "bronze",
    SILVER = "silver",
    GOLD = "gold",
    PLATINUM = "platinum",
}

export enum ProgressUnit {
    HOURS = "hours",
    DAYS = "days",
    BLOCKS = "blocks",
}

export interface TierRequirement {
    value: number; // hours, days, or blocks depending on milestone type
    coins: number;
    claimed?: boolean;
}

export interface Milestone {
    id: string;
    title: string;
    description: string;
    tiers: Record<TierName, TierRequirement>;
    progressUnit: ProgressUnit;
}


export enum ChallengeType {
    DAILY = "daily",
    SPECIAL = "special",
    MILESTONE = "milestone",
}

export interface Challenge {
    id: string;
    title: string;
    description: string;
    coins: number;
    goal: number;
    challengeType: ChallengeType;
    isLimited?: boolean;
    expiresIn?: number; // in seconds
}


import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import apiClient from '@/api/apiClient';
import { useRouter } from 'vue-router';

import type { User, ChallengeProgress, MilestoneProgress, StudyStat } from '../models/User';
import type { ShopItem } from '../models/ShopItem';
import type { StudySession } from '../models/StudySession';

const backendUrl = import.meta.env.VITE_FAST_API_URI;

export const useUserStore = defineStore('user', () => {
  const router = useRouter();
  const user = ref<User | null>(null);
  const blockedSites = ref<string[]>([]);
  const challenges = ref<ChallengeProgress[]>([]);
  const milestones = ref<MilestoneProgress[]>([]);
  const purchasedItems = ref<ShopItem[]>([]);
  const studyStats = ref<StudyStat[]>([]);
  const isPhoneLockEnabled = ref(false);
  const focusTime = ref(0);
  const dayStreak = ref(0);
  const weeklyStudyHours = ref(0);
  const monthlyStudyHours = ref(0);
  const coins = ref(0);
  const studySessions = ref<StudySession[]>([]);

  const isLoggedIn = computed(() => !!user.value);

  const fetchUserData = async () => {
    try {
      const response = await apiClient.get<any>(`/users/me`)
      const d = response.data

      user.value = {
        id: d._id,
        name: d.name,
        email: d.email,
        coins: d.coins,
        dayStreak: d.day_streak,
        longestStreak: d.longest_streak,
        lastActiveDate: d.last_active_date,
        challenges: d.challenges,
        milestones: d.milestones,
        purchasedItems: d.purchased_items,
        blockedWebsites: d.blocked_websites,
        totalFocusTime: d.total_focus_time,
        weeklyFocusTime: d.weekly_focus_time,
        monthlyFocusTime: d.monthly_focus_time,
        studyStats: d.study_stats,
        isPhoneLockEnabled: d.is_phone_lock_enabled ?? false,
        isActive: d.is_active,
        role: d.role,
        lastLogin: d.last_login
      }

      // now populate your other refs off that same `user.value`
      blockedSites.value = user.value.blockedWebsites
      challenges.value = user.value.challenges
      milestones.value = user.value.milestones
      purchasedItems.value = user.value.purchasedItems
      studyStats.value = user.value.studyStats
      focusTime.value = user.value.totalFocusTime
      dayStreak.value = user.value.dayStreak
      weeklyStudyHours.value = user.value.weeklyFocusTime
      monthlyStudyHours.value = user.value.monthlyFocusTime
      coins.value = user.value.coins
      isPhoneLockEnabled.value = user.value.isPhoneLockEnabled

    } catch (error) {
      console.error('Error fetching user data:', error)
    }
  }

  const initializeStore = async () => {
    if (localStorage.getItem('access_token')) {
      try {
        await fetchUserData();
      } catch (error) {
        console.error('Error initializing store:', error);
      }
    }
  };

  // Call initializeStore when the store is created
  initializeStore();

  const fetchStudySessions = async () => {
    try {
      const { data } = await apiClient.get<StudySession[]>('/study-sessions');
      studySessions.value = data;
    } catch (error) {
      console.error('Error fetching study sessions:', error);
    }
  };

  const createStudySession = async (session: Partial<StudySession>) => {
    try {
      const response = await apiClient.post(`/users/${user.value?.id}/study-sessions`, session);
      studySessions.value.push(response.data);
    } catch (error) {
      console.error('Error creating study session:', error);
    }
  };

  const updateStudySession = async (sessionId: string, updates: Partial<StudySession>) => {
    try {
      const response = await apiClient.patch(`/users/${user.value?.id}/study-sessions/${sessionId}`, updates);
      const index = studySessions.value.findIndex((s) => s._id === sessionId);
      if (index !== -1) {
        studySessions.value[index] = response.data;
      }
    } catch (error) {
      console.error('Error updating study session:', error);
    }
  };

  const addCoins = async (amount: number) => {
    try {
      const response = await apiClient.post(`/users/${user.value?.id}/add-coins`, { amount });
      user.value = response.data;
      coins.value = response.data.coins;
    } catch (error) {
      console.error('Error adding coins:', error);
    }
  };

  const updateChallengeProgress = async (challengeId: string, progress: number) => {
    try {
      const response = await apiClient.post(`/users/${user.value?.id}/challenges/${challengeId}/progress`, { progress });
      const updatedChallenge = response.data;
      const index = challenges.value.findIndex((c) => c.challenge_id === challengeId);
      if (index !== -1) {
        challenges.value[index] = updatedChallenge;
      } else {
        challenges.value.push(updatedChallenge);
      }
    } catch (error) {
      console.error('Error updating challenge progress:', error);
    }
  };

  const claimMilestoneTier = async (_id: string, tierName: string) => {
    try {
      const response = await apiClient.post(`/users/${user.value?.id}/milestones/${_id}/claim-tier`, { tier_name: tierName });
      console.log(response.data.message);
      await fetchUserData();
    } catch (error) {
      console.error('Error claiming milestone tier:', error);
    }
  };

  const purchaseShopItem = async (itemId: string) => {
    try {
      const response = await apiClient.post(`/users/${user.value?.id}/shop/items/${itemId}/purchase`);
      console.log(response.data.message);
      await fetchUserData();
    } catch (error) {
      console.error('Error purchasing shop item:', error);
    }
  };

  const updateFocusTime = async (minutes: number) => {
    try {
      await apiClient.post(`/users/${user.value?.id}/stats/update-focus`, { minutes });
      await fetchUserData();
    } catch (error) {
      console.error('Error updating focus time:', error);
    }
  };

  const addBlockedSite = async (site: string) => {
    try {
      await apiClient.post(`/users/${user.value?.id}/blocked-websites/add`, { website: site });
      blockedSites.value.push(site);
      console.log(`Blocked site "${site}" added successfully.`);
    } catch (error) {
      console.error('Error adding blocked site:', error);
    }
  };

  const removeBlockedSite = async (site: string) => {
    try {
      await apiClient.delete(`/users/${user.value?.id}/blocked-websites/remove`, {
        params: { website: site } // Send as query parameter
      });
      blockedSites.value = blockedSites.value.filter((s) => s !== site);
      console.log(`Blocked site "${site}" removed successfully.`);
    } catch (error) {
      console.error('Error removing blocked site:', error);
    }
  };

  const logout = () => {
    user.value = null;
    blockedSites.value = [];
    challenges.value = [];
    milestones.value = [];
    purchasedItems.value = [];
    studyStats.value = [];
    isPhoneLockEnabled.value = false;
    focusTime.value = 0;
    dayStreak.value = 0;
    weeklyStudyHours.value = 0;
    monthlyStudyHours.value = 0;
    coins.value = 0;
    studySessions.value = [];
    console.log('Logged out locally');
    router.push('/login'); // Redirect to login page
  };

  return {
    user,
    blockedSites,
    challenges,
    milestones,
    purchasedItems,
    studyStats,
    isPhoneLockEnabled,
    focusTime,
    dayStreak,
    weeklyStudyHours,
    monthlyStudyHours,
    coins,
    studySessions,
    isLoggedIn,
    fetchUserData,
    fetchStudySessions,
    createStudySession,
    updateStudySession,
    addCoins,
    updateChallengeProgress,
    claimMilestoneTier,
    purchaseShopItem,
    updateFocusTime,
    addBlockedSite,
    removeBlockedSite,
    logout,
  };
});

// src/api/studySessionService.ts
import apiClient from './apiClient';
import type { StudySession } from '@/models/StudySession';
import type { Task } from '@/models/Task';

export default {
  async getStudySessions(userId: string): Promise<StudySession[]> {
    const response = await apiClient.get('/study-sessions/', {
      params: { user_id: userId }
    });
    return response.data;
  },

  async createStudySession(
    userId: string,
    tasks: Task[],
    plannedDuration: number
  ): Promise<StudySession> {
    const response = await apiClient.post('/study-sessions/', {
      user_id: userId,
      tasks,
      planned_duration: plannedDuration
    });
    return response.data;
  },

  async completeStudySession(
    sessionId: string,
    actual_duration: number,
    distractionsBlocked: number = 0,
    notes?: string
  ): Promise<void> {
    await apiClient.post(`/study-sessions/${sessionId}/complete`, {
      actual_duration: actual_duration,
      distractions_blocked: distractionsBlocked,
      notes
    });
  }
};
i trust you to make it look amazing, also here is my color palette for this project:
cdb4db
ffc8dd
ffafcc
bde0fe
a2d2ff