import type { ShopItem } from './ShopItem';
import type { TierName } from './Milestone';

export interface ChallengeProgress {
    challengeId: string; // ID of the challenge
    progress: number;
    isCompleted: boolean;
    lastUpdated: string; // ISO string
}

export interface MilestoneProgress {
    milestoneId: string; // ID of the milestone
    progress: number;
    currentTier?: TierName;
    nextGoal?: number;
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
