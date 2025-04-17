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
      const index = studySessions.value.findIndex((s) => s.id === sessionId);
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
      const index = challenges.value.findIndex((c) => c.challengeId === challengeId);
      if (index !== -1) {
        challenges.value[index] = updatedChallenge;
      } else {
        challenges.value.push(updatedChallenge);
      }
    } catch (error) {
      console.error('Error updating challenge progress:', error);
    }
  };

  const claimMilestoneTier = async (milestoneId: string, tierName: string) => {
    try {
      const response = await apiClient.post(`/users/${user.value?.id}/milestones/${milestoneId}/claim-tier`, { tier_name: tierName });
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
    } catch (error) {
      console.error('Error adding blocked site:', error);
    }
  };

  const removeBlockedSite = async (site: string) => {
    try {
      await apiClient.delete(`/users/${user.value?.id}/blocked-websites/remove`, { data: { website: site } });
      blockedSites.value = blockedSites.value.filter((s) => s !== site);
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