import type { Task } from './Task';

export interface StudySession {
    _id: string;
    userId: string;
    tasks: Task[];
    plannedDuration: number; // in minutes
    actual_duration?: number; // in minutes
    startTime: string; // ISO string
    endTime?: string; // ISO string
    distractionsBlocked: number;
    notes?: string;
}
