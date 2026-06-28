import { AUTH_API_URL } from '../constants/api';
import { requestApi } from './api';
import type { User } from '../types';

interface LoginResponse {
  access_token: string;
}

export async function loginUser(email: string, password: string): Promise<LoginResponse> {
  return requestApi<LoginResponse>(AUTH_API_URL, '/auth/login', {
    method: 'POST',
    useAuth: false,
    body: JSON.stringify({ email, password }),
  });
}

export async function registerUser(email: string, username: string, password: string): Promise<User> {
  return requestApi<User>(AUTH_API_URL, '/auth/register', {
    method: 'POST',
    useAuth: false,
    body: JSON.stringify({ email, username, password }),
  });
}

interface VerifyTokenResponse {
  user_id: string;
}

export async function verifyToken(token: string): Promise<VerifyTokenResponse> {
  return requestApi<VerifyTokenResponse>(AUTH_API_URL, '/token/verify', {
    method: 'POST',
    useAuth: false, // pass token in body explicitly
    body: JSON.stringify({ token }),
  });
}
