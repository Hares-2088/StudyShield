import apiClient from './apiClient';
import type { Milestone } from '@/models/Milestone';

export default {
    async getMilestones(): Promise<Milestone[]> {
        const response = await apiClient.get('/milestones/');
        return response.data;
    },

    async getMilestoneById(milestoneId: string): Promise<Milestone> {
        const response = await apiClient.get(`/milestones/${milestoneId}`);
        return response.data;
    },

    async createMilestone(milestone: Partial<Milestone>): Promise<Milestone> {
        const response = await apiClient.post('/milestones/', milestone);
        return response.data;
    },

    async seedDefaultMilestones(): Promise<void> {
        await apiClient.post('/milestones/seed-default');
    },
};
