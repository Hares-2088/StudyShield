import apiClient from './apiClient';
import type { Milestone } from '@/models/Milestone';

export default {
  _normalize(m: any): Milestone {
    return {
      id:           m._id,
      title:        m.title,
      description:  m.description,
      tiers:        m.tiers,
      progressUnit: m.progress_unit,
    };
  },

  async getMilestones(): Promise<Milestone[]> {
    const { data } = await apiClient.get('/milestones/');
    return data.map((m: any) => this._normalize(m));
  },

  async getMilestoneById(_id: string): Promise<Milestone> {
    const { data } = await apiClient.get(`/milestones/${_id}`);
    return this._normalize(data);
  },

  async createMilestone(milestone: Partial<Milestone>): Promise<Milestone> {
    const { data } = await apiClient.post('/milestones/', milestone);
    return this._normalize(data);
  },

  async seedDefaultMilestones(): Promise<void> {
    await apiClient.post('/milestones/seed-default');
  },
};
