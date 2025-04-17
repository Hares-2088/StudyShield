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
