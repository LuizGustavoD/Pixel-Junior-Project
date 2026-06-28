import { TOKEN_STORAGE_KEY } from '../constants/api';

export class ApiError extends Error {
  code?: string;
  status: number;

  constructor(message: string, status: number, code?: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
  }
}

interface RequestOptions extends RequestInit {
  useAuth?: boolean;
}

export async function requestApi<T>(
  baseUrl: string,
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { useAuth = true, headers = {}, ...restOptions } = options;

  const url = `${baseUrl}${endpoint}`;

  const requestHeaders = new Headers(headers);

  if (useAuth) {
    const token = localStorage.getItem(TOKEN_STORAGE_KEY);
    if (token) {
      requestHeaders.set('Authorization', `Bearer ${token}`);
    }
  }

  // Auto-set content type if not multipart/form-data (fetch handles boundary automatically if omitted)
  if (!requestHeaders.has('Content-Type') && !(restOptions.body instanceof FormData)) {
    requestHeaders.set('Content-Type', 'application/json');
  }

  const response = await fetch(url, {
    headers: requestHeaders,
    ...restOptions,
  });

  const contentType = response.headers.get('Content-Type');
  let data: any;

  if (contentType && contentType.includes('application/json')) {
    data = await response.json();
  } else {
    data = await response.text();
  }

  if (!response.ok) {
    const errorMessage = data?.error?.message || data?.message || 'Ocorreu um erro na requisição.';
    const errorCode = data?.error?.code || 'API_ERROR';
    throw new ApiError(errorMessage, response.status, errorCode);
  }

  // If the backend returns a success/data envelope, unwrap it
  if (data && typeof data === 'object' && 'success' in data) {
    if (!data.success) {
      const errorMessage = data.error?.message || data.message || 'Operação malsucedida.';
      const errorCode = data.error?.code || 'BUSINESS_ERROR';
      throw new ApiError(errorMessage, response.status, errorCode);
    }
    return data.data as T;
  }

  return data as T;
}
