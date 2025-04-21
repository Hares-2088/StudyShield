// src/api/studySessionService.ts
import apiClient from './apiClient';
import type { StudySession } from '@/models/StudySession';
import type { Task } from '@/models/Task';

export default {
  async getStudySessions(userId: string): Promise<StudySession[]> {
    const response = await apiClient.get('/study-sessions/', {
      params: { user_id: userId }
    });
    return response.data;
  },

  async createStudySession(
    userId: string,
    tasks: Task[],
    plannedDuration: number
  ): Promise<StudySession> {
    const response = await apiClient.post('/study-sessions/', {
      user_id: userId,
      tasks,
      planned_duration: plannedDuration
    });
    return response.data;
  },

  async completeStudySession(
    sessionId: string,
    actual_duration: number,
    distractionsBlocked: number = 0,
    notes?: string
  ): Promise<void> {
    await apiClient.post(`/study-sessions/${sessionId}/complete`, {
      actual_duration: actual_duration,
      distractions_blocked: distractionsBlocked,
      notes
    });
  }
};