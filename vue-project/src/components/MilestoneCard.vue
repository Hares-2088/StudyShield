<template>
    <div class="bg-white rounded-lg shadow-md overflow-hidden border border-pink-100">
        <div class="bg-gradient-to-r from-pink-50 to-purple-50 p-4">
            <h3 class="text-lg font-semibold text-pink-800">{{ milestone.title }}</h3>
            <p class="text-sm text-gray-800">{{ milestone.description }}</p>
        </div>

        <div class="p-4">
            <!-- Progress bar -->
            <div class="mb-4">
                <div class="flex justify-between text-sm mb-1">
                    <span class="text-pink-800">Progress: {{ milestone.progress }} {{ getProgressUnit() }}</span>
                    <span v-if="milestone.next_goal" class="text-pink-700">Goal: {{ milestone.next_goal }} {{
                        getProgressUnit() }}</span>
                </div>
                <Progress :value="milestone.next_goal ? (milestone.progress / milestone.next_goal) * 100 : 100" />
            </div>

            <!-- Tiers display -->
            <div class="space-y-3">
                <div v-for="(tier, index) in milestone.tiers" :key="tier.name" class="border rounded-lg p-3" :class="{
                    'bg-gray-100': milestone.current_tier === 'none',
                    'bg-amber-100': tier.name === 'bronze' && milestone.current_tier === 'bronze',
                    'bg-gray-200': tier.name === 'silver' && milestone.current_tier === 'silver',
                    'bg-yellow-100': tier.name === 'gold' && milestone.current_tier === 'gold',
                    'bg-blue-100': tier.name === 'platinum' && milestone.current_tier === 'platinum',
                }">
                    <div class="flex justify-between items-center">
                        <div class="flex items-center">
                            <span class="mr-2">
                                {{ getTierEmoji(tier.name) }}
                            </span>
                            <span class="font-medium capitalize text-gray-900">{{ tier.name }}</span>
                        </div>

                        <div class="flex items-center">
                            <span class="text-lg mr-1">🪙</span>
                            <span class="font-semibold text-gray-900">{{ tier.coins }}</span>
                        </div>
                    </div>

                    <div class="mt-2 text-sm text-gray-700">
                        {{ getRequirementText(tier) }}
                    </div>

                    <button v-if="canClaimTier(tier)" @click="claimReward(tier)"
                        class="mt-2 w-full py-1.5 bg-pink-500 text-white text-sm rounded-lg hover:bg-pink-600 transition-colors">
                        Claim Reward
                    </button>

                    <p v-else-if="tier.claimed" class="mt-2 text-sm text-green-700 font-medium">
                        Reward Claimed ✓
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import Progress from './ui/progress/Progress.vue';

const props = defineProps({
    milestone: {
        type: Object,
        required: true
    }
});

const emit = defineEmits(['claim']);

// Get appropriate emoji for tier
const getTierEmoji = (tierName: string) => {
    switch (tierName) {
        case 'bronze': return '🥉';
        case 'silver': return '🥈';
        case 'gold': return '🥇';
        case 'platinum': return '💎';
        default: return '🏅';
    }
};

// Get requirement text based on milestone type
const getRequirementText = (tier: any) => {
    // Check which property exists on the tier to determine the milestone type
    if ('hours' in tier) {
        return `Study for ${tier.hours} total hours`;
    } else if ('streak' in tier) {
        return `Maintain a ${tier.streak}-day study streak`;
    } else if ('blocks' in tier) {
        return `Block distractions ${tier.blocks} times`;
    }
    return '';
};

// Get unit for progress (hours, days, blocks)
const getProgressUnit = () => {
    if (props.milestone.id.includes('time')) {
        return 'hours';
    } else if (props.milestone.id.includes('streak') || props.milestone.id.includes('consistency')) {
        return 'days';
    } else if (props.milestone.id.includes('distraction')) {
        return 'blocks';
    }
    return '';
};

// Check if tier can be claimed
const canClaimTier = (tier: any) => {
    // Get the property that matters for this milestone
    const propertyToCheck = Object.keys(tier).find(key =>
        ['hours', 'streak', 'blocks'].includes(key)
    );

    if (!propertyToCheck) return false;

    // Check if tier requirements are met and not already claimed
    return props.milestone.progress >= tier[propertyToCheck] &&
        !tier.claimed &&
        getTierValue(props.milestone.current_tier) >= getTierValue(tier.name);
};

// Get numeric value of tier for comparison
const getTierValue = (tierName: string) => {
    switch (tierName) {
        case 'none': return 0;
        case 'bronze': return 1;
        case 'silver': return 2;
        case 'gold': return 3;
        case 'platinum': return 4;
        default: return 0;
    }
};

// Claim reward for a tier
const claimReward = (tier: any) => {
    emit('claim', props.milestone.id, tier.name);
};
</script>
