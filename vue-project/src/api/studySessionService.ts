// src/api/studySessionService.ts
import apiClient from './apiClient';
import type { StudySession, RawStudySession } from '@/models/StudySession';
import type { Task } from '@/models/Task';

function mapSession(raw: RawStudySession): StudySession {
  return {
    _id: raw._id,
    userId: raw.user,
    tasks: raw.tasks,
    plannedDuration: raw.planned_duration,
    actualDuration: raw.actual_duration,
    startTime: raw.start_time,
    endTime: raw.end_time,
    isPaused: raw.is_paused,
    pausedAt: raw.paused_at,
    totalPaused: raw.total_paused,
    lastHeartbeat: raw.last_heartbeat,
    distractionsBlocked: raw.distractions_blocked,
    notes: raw.notes,
  };
}

export default {
  async getStudySessions(userId: string): Promise<StudySession[]> {
    const response = await apiClient.get('/study-sessions/', {
      params: { user_id: userId }
    });
    // Map each session
    return response.data.map(mapSession);
  },

  async getStudySession(sessionId: string): Promise<StudySession> {
    const response = await apiClient.get(`/study-sessions/${sessionId}`);
    // Map the session
    return mapSession(response.data);
  },


  async createStudySession(tasks: Task[], plannedDuration: number): Promise<StudySession> {
    console.log("service → POST /study-sessions/ body:", { tasks, planned_duration: plannedDuration });
    try {
      const resp = await apiClient.post<RawStudySession>('/study-sessions/', {
        tasks,
        planned_duration: plannedDuration,
      });
      console.log("service ← raw response data:", resp.data);
      const mapped = mapSession(resp.data);
      console.log("service → mapped session:", mapped);
      return mapped;
    } catch (err: any) {
      console.error("service ✖ error posting study-session:", err.response?.data || err);
      throw err;
    }
  },

  async completeStudySession(
    sessionId: string,
    actual_duration: number,
    distractions_blocked = 0,
    notes?: string
  ) {
    await apiClient.post(`/study-sessions/${sessionId}/complete`, {
      actual_duration,
      distractions_blocked,
      notes,
    });
  }
};