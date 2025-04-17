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
