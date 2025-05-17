import type { Task } from './Task';

export interface RawStudySession {
  _id: string;
  user: string;                  // Link<User> comes back as an OID string
  tasks: Task[];
  planned_duration: number;
  actual_duration?: number;
  start_time: string;
  end_time?: string;
  is_paused: boolean;
  paused_at?: string;
  total_paused: number;          // seconds
  last_heartbeat: string;
  distractions_blocked: number;
  notes?: string;
}

export interface StudySession {
  _id: string;
  userId: string;
  tasks: Task[];
  plannedDuration: number;
  actualDuration?: number;
  startTime: string;
  endTime?: string;
  isPaused: boolean;
  pausedAt?: string;
  totalPaused: number;
  lastHeartbeat: string;
  distractionsBlocked: number;
  notes?: string;
}