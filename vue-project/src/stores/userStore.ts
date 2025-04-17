import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import axios from 'axios';
import type { User, ChallengeProgress, MilestoneProgress, StudyStat } from '../models/User';
import type { ShopItem } from '../models/ShopItem';
import type { StudySession } from '../models/StudySession';

const backendUrl = import.meta.env.VITE_FAST_API_URI; // Use Vite's environment variable system

export const useUserStore = defineStore('user', () => {
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

  const fetchUserData = async (userId: string) => {
    try {
      const response = await axios.get(`${backendUrl}/users/${userId}`);
      user.value = response.data;
      blockedSites.value = response.data.blockedSites || [];
      challenges.value = response.data.challenges || [];
      milestones.value = response.data.milestones || [];
      purchasedItems.value = response.data.purchasedItems || [];
      studyStats.value = response.data.studyStats || [];
      isPhoneLockEnabled.value = response.data.isPhoneLockEnabled || false;
      focusTime.value = response.data.focusTime || 0;
      dayStreak.value = response.data.dayStreak || 0;
      weeklyStudyHours.value = response.data.weeklyStudyHours || 0;
      monthlyStudyHours.value = response.data.monthlyStudyHours || 0;
      coins.value = response.data.coins || 0;
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  const fetchStudySessions = async (userId: string) => {
    try {
      const response = await axios.get(`${backendUrl}/users/${userId}/study-sessions`);
      studySessions.value = response.data;
    } catch (error) {
      console.error('Error fetching study sessions:', error);
    }
  };

  const createStudySession = async (session: Partial<StudySession>) => {
    try {
      const response = await axios.post(`${backendUrl}/users/${user.value?.id}/study-sessions`, session);
      studySessions.value.push(response.data);
    } catch (error) {
      console.error('Error creating study session:', error);
    }
  };

  const updateStudySession = async (sessionId: string, updates: Partial<StudySession>) => {
    try {
      const response = await axios.patch(`${backendUrl}/users/${user.value?.id}/study-sessions/${sessionId}`, updates);
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
      const response = await axios.post(`${backendUrl}/users/${user.value?.id}/add-coins`, { amount });
      user.value = response.data;
      coins.value = response.data.coins;
    } catch (error) {
      console.error('Error adding coins:', error);
    }
  };

  const updateChallengeProgress = async (challengeId: string, progress: number) => {
    try {
      const response = await axios.post(`${backendUrl}/users/${user.value?.id}/challenges/${challengeId}/progress`, { progress });
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
      const response = await axios.post(`${backendUrl}/users/${user.value?.id}/milestones/${milestoneId}/claim-tier`, { tier_name: tierName });
      console.log(response.data.message);
      await fetchUserData(user.value?.id || '');
    } catch (error) {
      console.error('Error claiming milestone tier:', error);
    }
  };

  const purchaseShopItem = async (itemId: string) => {
    try {
      const response = await axios.post(`${backendUrl}/users/${user.value?.id}/shop/items/${itemId}/purchase`);
      console.log(response.data.message);
      await fetchUserData(user.value?.id || '');
    } catch (error) {
      console.error('Error purchasing shop item:', error);
    }
  };

  const updateFocusTime = async (minutes: number) => {
    try {
      await axios.post(`${backendUrl}/users/${user.value?.id}/stats/update-focus`, { minutes });
      await fetchUserData(user.value?.id || '');
    } catch (error) {
      console.error('Error updating focus time:', error);
    }
  };

  const addBlockedSite = async (site: string) => {
    try {
      await axios.post(`${backendUrl}/users/${user.value?.id}/blocked-websites/add`, { website: site });
      blockedSites.value.push(site);
    } catch (error) {
      console.error('Error adding blocked site:', error);
    }
  };

  const removeBlockedSite = async (site: string) => {
    try {
      await axios.delete(`${backendUrl}/users/${user.value?.id}/blocked-websites/remove`, { data: { website: site } });
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