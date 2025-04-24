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
    focus_time: number; // in minutes
    sessions: number;
    distractions_blocked: number;
}

export interface User {
    id: string;
    name: string;
    email: string;
    coins: number;
    dayStreak: number;
    longestStreak: number;
    streak_multiplier: number;
    lastActiveDate?: string; // ISO string
    challenges: ChallengeProgress[];
    milestones: MilestoneProgress[];
    purchasedItems: ShopItem[];
    blockedWebsites: string[];          // matches the API field
    totalFocusTime: number; // in minutes
    todayFocusTime: number; // in minutes
    weeklyFocusTime: number;
    monthlyFocusTime: number;
    studyStats: StudyStat[];
    isPhoneLockEnabled: boolean;
    isActive?: boolean; // Optional, for admin functionality
    role?: 'user' | 'admin'; // Optional, for role-based functionality
    lastLogin?: string; // ISO string, optional
}
