import { RESOURCE_API_URL, TOKEN_STORAGE_KEY } from '../constants/api';
import { requestApi } from './api';
import type { FileMetadata } from '../types';

export async function listFiles(): Promise<FileMetadata[]> {
  return requestApi<FileMetadata[]>(RESOURCE_API_URL, '/files', {
    method: 'GET',
  });
}

export async function deleteFile(fileId: string): Promise<void> {
  await requestApi<void>(RESOURCE_API_URL, `/files/delete/${fileId}`, {
    method: 'DELETE',
  });
}

export async function downloadFile(fileId: string, filename: string): Promise<void> {
  const token = localStorage.getItem(TOKEN_STORAGE_KEY);
  if (!token) {
    throw new Error('Sessão expirada. Faça login novamente.');
  }

  const response = await fetch(`${RESOURCE_API_URL}/files/download/${fileId}`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    let errorMessage = 'Erro ao baixar arquivo.';
    try {
      const errorJson = await response.json();
      errorMessage = errorJson.error?.message || errorJson.message || errorMessage;
    } catch {
      // ignore
    }
    throw new Error(errorMessage);
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}

export function uploadFile(
  file: File,
  onProgress: (progress: number) => void
): Promise<FileMetadata> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    formData.append('file', file);

    xhr.open('POST', `${RESOURCE_API_URL}/files/upload`);
    
    const token = localStorage.getItem(TOKEN_STORAGE_KEY);
    if (token) {
      xhr.setRequestHeader('Authorization', `Bearer ${token}`);
    }

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        const percentComplete = Math.round((event.loaded / event.total) * 100);
        onProgress(percentComplete);
      }
    };

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const res = JSON.parse(xhr.responseText);
          if (res.success) {
            resolve(res.data);
          } else {
            reject(new Error(res.error?.message || 'Falha no upload.'));
          }
        } catch {
          reject(new Error('Resposta inválida do servidor.'));
        }
      } else {
        try {
          const res = JSON.parse(xhr.responseText);
          reject(new Error(res.error?.message || 'Erro ao enviar arquivo.'));
        } catch {
          reject(new Error(`Erro ${xhr.status} ao enviar arquivo.`));
        }
      }
    };

    xhr.onerror = () => {
      reject(new Error('Erro de conexão ou rede.'));
    };

    xhr.send(formData);
  });
}

export async function getFilePreviewUrl(fileId: string): Promise<string> {
  const token = localStorage.getItem(TOKEN_STORAGE_KEY);
  if (!token) {
    throw new Error('Sessão expirada. Faça login novamente.');
  }

  const response = await fetch(`${RESOURCE_API_URL}/files/download/${fileId}`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    throw new Error('Erro ao carregar pré-visualização do arquivo.');
  }

  const blob = await response.blob();
  return window.URL.createObjectURL(blob);
}

