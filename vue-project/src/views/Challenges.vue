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

        <!-- Milestone Challenges Section -->
        <section>
            <h2 class="text-xl md:text-2xl font-bold text-pink-700 mb-4">Milestone Achievements</h2>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <MilestoneCard v-for="milestone in milestones" :key="milestone.id" :milestone="milestone"
                    @claim="claimMilestoneReward" />
            </div>
        </section>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '../stores/userStore';
import ChallengeCard from '../components/ChallengeCard.vue';
import MilestoneCard from '../components/MilestoneCard.vue';

const userStore = useUserStore();
const dayStreak = computed(() => userStore.dayStreak || 0);
const focusTime = computed(() => userStore.focusTime || 0);
const weeklyHours = computed(() => userStore.weeklyStudyHours || 0);

// Calculate streak bonus (1x, 1.5x, 2x, etc.)
const calculateBonus = () => {
    if (dayStreak.value >= 30) return 3;
    if (dayStreak.value >= 14) return 2;
    if (dayStreak.value >= 7) return 1.5;
    return 1;
};

// Challenge Data
const dailyChallenges = ref([
    {
        id: 'daily-1',
        title: 'Study Session',
        description: 'Complete a 25-minute focused study session',
        coins: 10,
        isCompleted: false,
        progress: 0,
        goal: 1
    },
    {
        id: 'daily-2',
        title: 'No Distractions',
        description: 'Block 3 distracting websites during study time',
        coins: 15,
        isCompleted: false,
        progress: 0,
        goal: 3
    },
    {
        id: 'daily-3',
        title: 'Morning Scholar',
        description: 'Study for at least 15 minutes before 10 AM',
        coins: 20,
        isCompleted: false,
        progress: 0,
        goal: 1
    },
    {
        id: 'daily-4',
        title: 'Study Marathon',
        description: 'Accumulate 2 hours of total study time today',
        coins: 30,
        isCompleted: false,
        progress: Math.min(focusTime.value, 120),
        goal: 120
    },
    {
        id: 'daily-5',
        title: 'Break Time',
        description: 'Take proper breaks between study sessions',
        coins: 15,
        isCompleted: false,
        progress: 0,
        goal: 3
    }
]);

const specialChallenges = ref([
    {
        id: 'special-1',
        title: 'Weekend Warrior',
        description: 'Complete 4 hours of study on a weekend',
        coins: 50,
        isCompleted: false,
        limited: true,
        expiresIn: '2 days',
        progress: 0,
        goal: 240
    },
    {
        id: 'special-2',
        title: 'Subject Master',
        description: 'Study 3 different subjects in one day',
        coins: 40,
        isCompleted: false,
        limited: false,
        progress: 0,
        goal: 3
    },
    {
        id: 'special-3',
        title: 'Group Study',
        description: 'Invite a friend to study with you',
        coins: 35,
        isCompleted: false,
        limited: false,
        progress: 0,
        goal: 1
    }
]);

const milestones = ref([
    {
        id: 'milestone-1',
        title: 'Study Time Master',
        description: 'Accumulate study hours',
        currentTier: 'bronze',
        tiers: [
            { name: 'bronze', hours: 50, coins: 100, claimed: false },
            { name: 'silver', hours: 100, coins: 200, claimed: false },
            { name: 'gold', hours: 200, coins: 300, claimed: false },
            { name: 'platinum', hours: 500, coins: 500, claimed: false }
        ],
        progress: Math.floor(focusTime.value / 60), // Convert minutes to hours
        nextGoal: 50
    },
    {
        id: 'milestone-2',
        title: 'Consistency Champion',
        description: 'Maintain daily study streaks',
        currentTier: 'none',
        tiers: [
            { name: 'bronze', streak: 7, coins: 50, claimed: false },
            { name: 'silver', streak: 14, coins: 100, claimed: false },
            { name: 'gold', streak: 30, coins: 250, claimed: false },
            { name: 'platinum', streak: 60, coins: 500, claimed: false }
        ],
        progress: dayStreak.value,
        nextGoal: 7
    },
    {
        id: 'milestone-3',
        title: 'Distraction Defeater',
        description: 'Block websites during study sessions',
        currentTier: 'none',
        tiers: [
            { name: 'bronze', blocks: 25, coins: 75, claimed: false },
            { name: 'silver', blocks: 50, coins: 150, claimed: false },
            { name: 'gold', blocks: 100, coins: 300, claimed: false },
            { name: 'platinum', blocks: 250, coins: 500, claimed: false }
        ],
        progress: userStore.blockedSites.length * 5, // Estimate based on current blocked sites
        nextGoal: 25
    }
]);

// Update milestone progress and current tier
const updateMilestones = () => {
    milestones.value.forEach(milestone => {
        // Update Study Time Master milestone
        if (milestone.id === 'milestone-1') {
            const hours = Math.floor(focusTime.value / 60);
            milestone.progress = hours;

            if (hours >= 500) {
                milestone.currentTier = 'platinum';
                milestone.nextGoal = null;
            } else if (hours >= 200) {
                milestone.currentTier = 'gold';
                milestone.nextGoal = 500;
            } else if (hours >= 100) {
                milestone.currentTier = 'silver';
                milestone.nextGoal = 200;
            } else if (hours >= 50) {
                milestone.currentTier = 'bronze';
                milestone.nextGoal = 100;
            } else {
                milestone.currentTier = 'none';
                milestone.nextGoal = 50;
            }
        }

        // Update Consistency Champion milestone
        if (milestone.id === 'milestone-2') {
            milestone.progress = dayStreak.value;

            if (dayStreak.value >= 60) {
                milestone.currentTier = 'platinum';
                milestone.nextGoal = null;
            } else if (dayStreak.value >= 30) {
                milestone.currentTier = 'gold';
                milestone.nextGoal = 60;
            } else if (dayStreak.value >= 14) {
                milestone.currentTier = 'silver';
                milestone.nextGoal = 30;
            } else if (dayStreak.value >= 7) {
                milestone.currentTier = 'bronze';
                milestone.nextGoal = 14;
            } else {
                milestone.currentTier = 'none';
                milestone.nextGoal = 7;
            }
        }
    });
};

// Handle challenge completion
const completeChallenge = async (challengeId: string) => {
    const dailyChallenge = dailyChallenges.value.find(c => c.id === challengeId);
    const specialChallenge = specialChallenges.value.find(c => c.id === challengeId);

    if (dailyChallenge && !dailyChallenge.isCompleted) {
        const bonus = calculateBonus();
        const coinsEarned = Math.floor(dailyChallenge.coins * bonus);
        await userStore.addCoins(coinsEarned);
        dailyChallenge.isCompleted = true;
    } else if (specialChallenge && !specialChallenge.isCompleted) {
        await userStore.addCoins(specialChallenge.coins);
        specialChallenge.isCompleted = true;
    }
};

// Handle milestone reward claims
const claimMilestoneReward = async (milestoneId: string, tierName: string) => {
    const milestone = milestones.value.find(m => m.id === milestoneId);
    if (!milestone) return;

    const tier = milestone.tiers.find(t => t.name === tierName);
    if (tier && !tier.claimed) {
        await userStore.addCoins(tier.coins);
        tier.claimed = true;
    }
};

onMounted(() => {
    updateMilestones();
});
</script>
