import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import apiClient from '@/api/apiClient';
import { useRouter } from 'vue-router';

import type { User, ChallengeProgress, MilestoneProgress, StudyStat } from '../models/User';
import type { ShopItem } from '../models/ShopItem';
import type { StudySession } from '../models/StudySession'; // Assuming Task is part of StudySession or in its own file e.g., ../models/Task
import studySessionService from '../api/studySessionService'; // Assuming you have a service for handling study sessions
import type { Task } from '../models/Task'; // Assuming Task is part of StudySession or in its own file e.g., ../models/Task

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
  const streak_multiplier = ref(0);
  const weeklyStudyHours = ref(0);
  const todayFocusTime = ref(0);
  const monthlyStudyHours = ref(0);
  const coins = ref(0);
  const studySessions = ref<StudySession[]>([]);
  const currentSession = ref<StudySession | null>(null);

  const isLoggedIn = computed(() => !!user.value);

  let heartbeatHandle: number | null = null;

  // start sending a heartbeat every 10s
  function startHeartbeat() {
    stopHeartbeat();
    if (!currentSession.value) return;
    heartbeatHandle = window.setInterval(async () => {
      try {
        await apiClient.post(
          `/study-sessions/${currentSession.value!._id}/heartbeat`
        );
      } catch (e) {
        console.warn('Heartbeat failed', e);
      }
    }, 10_000);
  }

  // stop the heartbeat
  function stopHeartbeat() {
    if (heartbeatHandle !== null) {
      clearInterval(heartbeatHandle);
      heartbeatHandle = null;
    }
  }

  // pause the current session
  async function pauseCurrentSession() {
    if (!currentSession.value) return;
    await apiClient.post(
      `/study-sessions/${currentSession.value._id}/pause`
    );
    stopHeartbeat();
    // just flip the flag locally
    currentSession.value.isPaused = true;
  
    }

  // resume the current session
  async function resumeCurrentSession() {
    if (!currentSession.value) return;
    await apiClient.post(
      `/study-sessions/${currentSession.value!._id}/resume`
    );
    currentSession.value.isPaused = false;
    startHeartbeat();
  }


  const fetchUserData = async () => {
    try {
      const { data: d } = await apiClient.get<any>('/users/me');

      // 1) Turn your two DBRefs into actual ShopItem objects, safely:
      let detailedPurchasedItems: ShopItem[] = [];

      if (Array.isArray(d.purchased_items)) {
        // Try to fetch each one, but don’t let one 404/CORS drop kill the rest:
        const fetches = d.purchased_items.map(async (ref: any) => {
          // if it's already a full object, it'll have a .id and .title
          if (ref.id && ref.title) {
            return ref as ShopItem;
          }
          // otherwise assume it's a DBRef
          const itemId = ref.$id?.$oid ?? ref.$id;
          if (!itemId) return null;
          try {
            const res = await apiClient.get<ShopItem>(`/shop/items/${itemId}`);
            return res.data;
          } catch (err) {
            console.warn(`Couldn’t fetch ShopItem ${itemId}`, err);
            return null;
          }
        });
        const settled = await Promise.allSettled(fetches);
        detailedPurchasedItems = settled
          .filter((r): r is PromiseFulfilledResult<ShopItem> =>
            r.status === 'fulfilled' && !!r.value
          )
          .map(r => r.value!);
      }

      // 2) Build your User object exactly once
      user.value = {
        id: d._id,
        name: d.name,
        email: d.email,
        coins: d.coins,
        dayStreak: d.day_streak,
        longestStreak: d.longest_streak,
        streak_multiplier: d.streak_multiplier,
        lastActiveDate: d.last_active_date,
        challenges: d.challenges,
        milestones: d.milestones,
        purchasedItems: detailedPurchasedItems, // Correctly assign processed items
        blockedWebsites: d.blocked_websites,
        totalFocusTime: d.total_focus_time,
        todayFocusTime: d.today_focus_time,
        weeklyFocusTime: d.weekly_focus_time,
        monthlyFocusTime: d.monthly_focus_time,
        studyStats: d.study_stats,
        isPhoneLockEnabled: d.is_phone_lock_enabled ?? false,
        current_session: d.current_session,
        isActive: d.is_active,
        role: d.role,
        lastLogin: d.last_login
      };

      // 3) Push out into your store refs
      blockedSites.value = user.value.blockedWebsites;
      challenges.value = user.value.challenges;
      milestones.value = user.value.milestones;
      purchasedItems.value = detailedPurchasedItems; // Ensure this is correctly assigned
      studyStats.value = user.value.studyStats;
      focusTime.value = user.value.totalFocusTime;
      todayFocusTime.value = user.value.todayFocusTime;
      dayStreak.value = user.value.dayStreak;
      streak_multiplier.value = user.value.streak_multiplier;
      weeklyStudyHours.value = user.value.weeklyFocusTime;
      monthlyStudyHours.value = user.value.monthlyFocusTime;
      currentSession.value = user.value.current_session ?? null;
      coins.value = user.value.coins;

    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

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

  async function createStudySession(tasks: Task[]) {
    const planned = tasks.reduce((sum, t) => sum + t.duration, 0);

    console.log('store: about to call service.createStudySession with', tasks, 'planned=', planned);
    const session = await studySessionService.createStudySession(tasks, planned);
    console.log('store: got session back →', session);

    currentSession.value = session;
    startHeartbeat();

    return session;
  }

  // in completeStudySession (or in your finishSession call):
  async function completeStudySession(sessionId: string, actualMins: number) {
    stopHeartbeat();
    await studySessionService.completeStudySession(sessionId, actualMins, 0);
    currentSession.value = null;
    await fetchUserData();  // will clear it on the backend
  }

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

  const redeemChallenge = async (challengeId: string) => {
    try {
      await apiClient.post(`/users/${user.value?.id}/challenges/${challengeId}/redeem`);
      await fetchUserData(); // Refresh coins & progress
    } catch (error) {
      console.error('Error redeeming challenge:', error);
    }
  };

  const redeemMilestone = async (milestoneId: string, tier: string) => {
    try {
      await apiClient.post(`/users/${user.value?.id}/milestones/${milestoneId}/redeem/${tier}`);
      await fetchUserData(); // Refresh coins & progress
    } catch (error) {
      console.error('Error redeeming milestone:', error);
    }
  };

  const logout = () => {
    user.value = null;
    blockedSites.value = [];
    challenges.value = [];
    milestones.value = [];
    streak_multiplier.value = 0;
    purchasedItems.value = [];
    studyStats.value = [];
    isPhoneLockEnabled.value = false;
    focusTime.value = 0;
    dayStreak.value = 0;
    todayFocusTime.value = 0;
    weeklyStudyHours.value = 0;
    monthlyStudyHours.value = 0;
    currentSession.value = null;
    coins.value = 0;
    studySessions.value = [];
    console.log('Logged out locally');
    router.push('/login'); // Redirect to login page
  };

  return {
    user,
    blockedSites,
    streak_multiplier,
    challenges,
    milestones,
    purchasedItems,
    studyStats,
    isPhoneLockEnabled,
    focusTime,
    dayStreak,
    weeklyStudyHours,
    todayFocusTime,
    monthlyStudyHours,
    coins,
    currentSession,
    pauseCurrentSession,
    resumeCurrentSession,
    stopHeartbeat,
    startHeartbeat,
    createStudySession,
    completeStudySession,
    studySessions,
    isLoggedIn,
    fetchUserData,
    fetchStudySessions,
    updateStudySession,
    addCoins,
    updateChallengeProgress,
    claimMilestoneTier,
    purchaseShopItem,
    updateFocusTime,
    addBlockedSite,
    removeBlockedSite,
    redeemChallenge,
    redeemMilestone,
    logout,
  };
});