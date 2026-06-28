export interface User {
  id: string;
  email: string;
  username: string;
  created_at?: string;
}

export interface AuthState {
  token: string | null;
  user: User | null;
}

export interface FileMetadata {
  id: string;
  original_name: string;
  content_type: string;
  size: number;
  created_at: string;
}

export interface UploadProgressState {
  fileName: string;
  progress: number;
  status: 'idle' | 'uploading' | 'success' | 'error';
  error: string | null;
}
