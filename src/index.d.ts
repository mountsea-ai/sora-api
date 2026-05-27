/**
 * Mountsea Sora SDK - TypeScript Definitions
 *
 * Documentation: https://docs.mountsea.ai/api-reference/sora/introduction
 * Platform: https://offoff.ai/
 */

export interface SoraClientOptions {
  baseUrl?: string;
  timeout?: number;
}

export interface GenerateOptions {
  duration?: number;
  resolution?: string;
  imageUrl?: string;
  [key: string]: any;
}

export interface TaskResult {
  taskId: string;
  status: string;
  videoUrl?: string;
  error?: string;
}

export interface WaitOptions {
  timeout?: number;
  interval?: number;
}

export declare class SoraClient {
  constructor(apiKey: string, options?: SoraClientOptions);
  generate(prompt: string, options?: GenerateOptions): Promise<TaskResult>;
  imageToVideo(prompt: string, imageUrl: string, options?: GenerateOptions): Promise<TaskResult>;
  getTask(taskId: string): Promise<TaskResult>;
  wait(taskId: string, options?: WaitOptions): Promise<TaskResult>;
}

