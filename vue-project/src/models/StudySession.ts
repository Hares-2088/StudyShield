import type { Task } from './Task';

export interface StudySession {
    id: string;
    userId: string;
    tasks: Task[];
    plannedDuration: number; // in minutes
    actualDuration?: number; // in minutes
    startTime: string; // ISO string
    endTime?: string; // ISO string
    distractionsBlocked: number;
    notes?: string;
}
