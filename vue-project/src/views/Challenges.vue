<template>
  <div class="w-full p-0 md:p-6">
    <!-- Streak Banner -->
    <div class="bg-gradient-to-r from-[#FFAFCC] to-[#A2D2FF] rounded-lg p-4 mb-6 shadow-lg">
      <div class="flex flex-col md:flex-row justify-between items-center text-white">
        <div class="flex items-center mb-2 md:mb-0">
          <span class="text-2xl mr-2">🔥</span>
          <h1 class="text-xl md:text-2xl font-bold">{{ dayStreak }} Day Streak!</h1>
        </div>
        <div class="bg-white/20 px-4 py-2 rounded-lg backdrop-blur-sm border border-white/10">
          <p class="text-sm md:text-base">
            <span class="font-bold">{{ calculateBonus() }}x</span> Coin Bonus on Daily Challenges
          </p>
        </div>
      </div>
    </div>

    <!-- Streak Bonus Tiers -->
    <section class="mb-8">
      <h2 class="text-lg font-semibold text-gray-700 mb-2">Streak Bonus Tiers</h2>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div v-for="tier in streakTiers" :key="tier.label"
          class="bg-white/20 backdrop-blur-sm p-3 rounded-lg text-center">
          <p class="font-medium">{{ tier.label }}</p>
          <p class="text-xl font-bold">{{ tier.multiplier }}×</p>
        </div>
      </div>
    </section>

    <!-- Daily Challenges Section -->
    <section class="mb-8">
      <h2 class="text-xl md:text-2xl font-bold text-pink-700 mb-4">Daily Challenges</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <ChallengeCard v-for="challenge in dailyChallenges" :key="challenge.id" :challenge="challenge"
          :coinMultiplier="calculateBonus()" @complete="completeChallenge" />
      </div>
    </section>

    <!-- Special Challenges Section -->
    <section class="mb-8">
      <h2 class="text-xl md:text-2xl font-bold text-pink-700 mb-4">Special Challenges</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <ChallengeCard v-for="challenge in specialChallenges" :key="challenge.id" :challenge="challenge"
          @complete="completeChallenge" />
      </div>
    </section>

    <!-- Milestone Achievements Section -->
    <section>
      <h2 class="text-xl md:text-2xl font-bold text-pink-700 mb-4">Milestone Achievements</h2>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <MilestoneCard v-for="ms in mergedMilestones" :key="ms.id" :milestone="ms" @claim="claimMilestoneReward" />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '../stores/userStore';
import ChallengeCard from '../components/ChallengeCard.vue';
import MilestoneCard from '../components/MilestoneCard.vue';
import challengeApi from '@/api/challengeService';
import milestoneApi from '@/api/milestoneService';
import type { Challenge } from '@/models/Challenge';
import type { Milestone } from '@/models/Milestone';

// Store & raw definitions
const userStore = useUserStore();
const rawDailyDefs = ref<Challenge[]>([]);
const rawSpecialDefs = ref<Challenge[]>([]);
const milestoneDefs = ref<Milestone[]>([]);

// Computed merges for user progress + definitions
const dailyChallenges = computed(() =>
  rawDailyDefs.value.map(def => {
    const prog = userStore.challenges.find(
      cp => cp.challenge_id === def.id
    );
    return {
      ...def,
      progress: prog?.progress ?? 0,
      isCompleted: prog?.is_completed ?? false
    };
  })
);

const specialChallenges = computed(() =>
  rawSpecialDefs.value.map(def => {
    const prog = userStore.challenges.find(
      cp => cp.challenge_id === def.id
    );
    return {
      ...def,
      progress: prog?.progress ?? 0,
      isCompleted: prog?.is_completed ?? false
    };
  })
);

// Tier order map for milestone claimed logic
const tierOrder: Record<string, number> = {
  none: 0,
  bronze: 1,
  silver: 2,
  gold: 3,
  platinum: 4
};

const mergedMilestones = computed(() =>
  milestoneDefs.value.map(def => {
    const prog = userStore.milestones.find(
      mp => mp._id === def.id
    );
    const currentTier = prog?.current_tier ?? 'none';
    const nextGoal = prog?.next_goal ?? Object.values(def.tiers)[0].value;
    const progress = prog?.progress ?? 0;
    const tiers = Object.entries(def.tiers).map(([name, req]) => ({
      name,
      value: req.value,
      coins: req.coins,
      claimed: tierOrder[name] <= tierOrder[currentTier]
    }));
    return { id: def.id, title: def.title, description: def.description, tiers, progress, currentTier, nextGoal };
  })
);

// Fetch data
onMounted(async () => {
  try {
    rawDailyDefs.value = await challengeApi.getDailyChallenges();
    rawSpecialDefs.value = await challengeApi.getChallenges('special');
    milestoneDefs.value = await milestoneApi.getMilestones();
    await userStore.fetchUserData();
  } catch (err) {
    console.error('Error loading challenges/milestones:', err);
  }
});

// Streak & bonus
const dayStreak = computed(() => userStore.dayStreak || 0);
const calculateBonus = () => {
  if (dayStreak.value >= 30) return 3;
  if (dayStreak.value >= 14) return 2;
  if (dayStreak.value >= 7) return 1.5;
  return 1;
};
  
//  streak tiers lookup 
const streakTiers = [
  { label: '1–6 days', multiplier: 1 },
  { label: '7–13 days', multiplier: 1.5 },
  { label: '14–29 days', multiplier: 2 },
  { label: '30+ days', multiplier: 3 },
];


// Actions
const completeChallenge = async (id: string) => {
  try {
    await userStore.updateChallengeProgress(id, 1);
    await userStore.fetchUserData();
  } catch (err) {
    console.error('Failed to complete challenge:', err);
  }
};

const claimMilestoneReward = async (milestoneId: string, tierName: string) => {
  try {
    await userStore.claimMilestoneTier(milestoneId, tierName);
    await userStore.fetchUserData();
  } catch (err) {
    console.error('Failed to claim milestone reward:', err);
  }
};
</script>