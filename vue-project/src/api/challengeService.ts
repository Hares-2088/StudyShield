import apiClient from './apiClient';
import type { Challenge } from '@/models/Challenge';

export default {
  // normalize the backend payload
  _normalize(ch: any): Challenge {
    return {
      id:           ch._id,
      title:        ch.title,
      description:  ch.description,
      coins:        ch.coins,
      goal:         ch.goal,
      challengeType: ch.challenge_type,
      isLimited:    ch.is_limited,
      expiresIn:    ch.expires_in,
    };
  },

  async getChallenges(
    challengeType?: string,
    isLimited?: boolean
  ): Promise<Challenge[]> {
    const { data } = await apiClient.get('/challenges/', {
      params: { challenge_type: challengeType, is_limited: isLimited },
    });
    return data.map((c: any) => this._normalize(c));
  },

  async getDailyChallenges(): Promise<Challenge[]> {
    const { data } = await apiClient.get('/challenges/daily');
    return data.map((c: any) => this._normalize(c));
  },

  async getMilestoneChallenges(): Promise<Challenge[]> {
    const { data } = await apiClient.get('/challenges/milestones');
    return data.map((c: any) => this._normalize(c));
  },

  async getChallengeById(challengeId: string): Promise<Challenge> {
    const { data } = await apiClient.get(`/challenges/${challengeId}`);
    return this._normalize(data);
  },

  async createChallenge(challenge: Partial<Challenge>): Promise<Challenge> {
    const { data } = await apiClient.post('/challenges/', challenge);
    return this._normalize(data);
  },

  async seedDefaultDailyChallenges(): Promise<void> {
    await apiClient.post('/challenges/daily/seed-default');
  },
};
