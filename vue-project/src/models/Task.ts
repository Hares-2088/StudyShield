export interface Task {
  name: string;
  duration: number; // in minutes
  completed?: boolean;
}