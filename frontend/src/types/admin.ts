export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}

export interface AISettings {
  model: string;
  temperature: number;
  tokenLimit: number;
  promptTemplate: string;
}

export interface AuditLog {
  id: string;
  user: string;
  action: string;
  time: string;
}