import apiClient from './apiClient';
import type { Challenge } from '@/models/Challenge';

export default {
    async getChallenges(
        challengeType?: string,
        isLimited?: boolean
    ): Promise<Challenge[]> {
        const response = await apiClient.get('/challenges/', {
            params: {
                challenge_type: challengeType,
                is_limited: isLimited,
            },
        });
        return response.data;
    },

    async getDailyChallenges(): Promise<Challenge[]> {
        const response = await apiClient.get('/challenges/daily');
        return response.data;
    },

    async getMilestoneChallenges(): Promise<Challenge[]> {
        const response = await apiClient.get('/challenges/milestones');
        return response.data;
    },

    async getChallengeById(challengeId: string): Promise<Challenge> {
        const response = await apiClient.get(`/challenges/${challengeId}`);
        return response.data;
    },

    async createChallenge(challenge: Partial<Challenge>): Promise<Challenge> {
        const response = await apiClient.post('/challenges/', challenge);
        return response.data;
    },

    async seedDefaultDailyChallenges(): Promise<void> {
        await apiClient.post('/challenges/daily/seed-default');
    },
};
