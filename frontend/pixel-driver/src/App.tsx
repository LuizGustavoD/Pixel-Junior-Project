import { useState, useEffect, useCallback } from 'react';
import { ToastProvider, useToast } from './components/ui/Toast';
import { LoginForm } from './components/LoginForm';
import { RegisterForm } from './components/RegisterForm';
import { UploadForm } from './components/UploadForm';
import { FileList } from './components/FileList';
import { DashboardLayout } from './layouts/DashboardLayout';
import { verifyToken } from './services/auth';
import { listFiles, downloadFile, deleteFile } from './services/files';
import { TOKEN_STORAGE_KEY, USER_STORAGE_KEY } from './constants/api';
import type { User, FileMetadata } from './types';
import { Card } from './components/ui/Card';
import './App.css';

function AppContent() {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [files, setFiles] = useState<FileMetadata[]>([]);
  
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const [isLoadingFiles, setIsLoadingFiles] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const { showToast } = useToast();

  const handleLogout = useCallback(() => {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    localStorage.removeItem(USER_STORAGE_KEY);
    setToken(null);
    setUser(null);
    setFiles([]);
    showToast('Sessão encerrada com sucesso.', 'info');
  }, [showToast]);

  const loadUserFiles = useCallback(async () => {
    setIsLoadingFiles(true);
    try {
      const data = await listFiles();
      setFiles(data);
    } catch (err: any) {
      // If unauthorized, logout
      if (err.status === 401) {
        handleLogout();
      } else {
        showToast(err.message || 'Erro ao carregar arquivos.', 'error');
      }
    } finally {
      setIsLoadingFiles(false);
    }
  }, [handleLogout, showToast]);

  // Check auth on mount
  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem(TOKEN_STORAGE_KEY);
      if (storedToken) {
        try {
          const res = await verifyToken(storedToken);
          const storedUser = localStorage.getItem(USER_STORAGE_KEY);
          
          let currentUser: User;
          if (storedUser) {
            currentUser = JSON.parse(storedUser);
          } else {
            currentUser = {
              id: res.user_id,
              email: 'usuario@pixel.com',
              username: 'Usuário',
            };
          }
          
          setToken(storedToken);
          setUser(currentUser);
        } catch (err: any) {
          localStorage.removeItem(TOKEN_STORAGE_KEY);
          localStorage.removeItem(USER_STORAGE_KEY);
          showToast('Sessão expirada. Por favor, faça login novamente.', 'warning');
        }
      }
      setIsCheckingAuth(false);
    };

    initAuth();
  }, [showToast]);

  useEffect(() => {
    if (token) {
      loadUserFiles();
    }
  }, [token, loadUserFiles]);

  const handleLoginSuccess = async (newToken: string) => {
    const emailInput = document.querySelector('input[type="email"]') as HTMLInputElement;
    const email = emailInput?.value || 'usuario@pixel.com';
    const username = email.split('@')[0];

    try {
      const res = await verifyToken(newToken);
      const currentUser: User = {
        id: res.user_id,
        email,
        username,
      };

      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(currentUser));
      setUser(currentUser);
      setToken(newToken);
    } catch (err: any) {
      showToast('Erro ao validar sessão após login.', 'error');
      handleLogout();
    }
  };

  const handleFileDownload = async (fileId: string, filename: string) => {
    try {
      await downloadFile(fileId, filename);
      showToast('Download concluído!', 'success');
    } catch (err: any) {
      showToast(err.message || 'Erro ao fazer download do arquivo.', 'error');
    }
  };

  const handleFileDelete = async (fileId: string) => {
    try {
      await deleteFile(fileId);
      showToast('Arquivo deletado com sucesso.', 'success');
      // Refresh list
      loadUserFiles();
    } catch (err: any) {
      showToast(err.message || 'Erro ao deletar o arquivo.', 'error');
    }
  };

  if (isCheckingAuth) {
    return (
      <div className="app-checking-auth">
        <svg className="animate-spin" viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="var(--accent)" strokeWidth="3">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
        <span className="checking-text">Verificando sessão...</span>
      </div>
    );
  }

  if (!token) {
    return (
      <div className="auth-page-container">
        <div className="auth-background-decor"></div>
        <Card glass className="auth-card-wrapper">
          {showRegister ? (
            <RegisterForm
              onSuccess={() => setShowRegister(false)}
              onToggleForm={() => setShowRegister(false)}
            />
          ) : (
            <LoginForm
              onSuccess={handleLoginSuccess}
              onToggleForm={() => setShowRegister(true)}
            />
          )}
        </Card>
      </div>
    );
  }

  return (
    <DashboardLayout user={user} onLogout={handleLogout}>
      <div className="dashboard-grid">
        <div className="upload-section">
          <UploadForm onUploadSuccess={loadUserFiles} />
        </div>
        <div className="files-section">
          <FileList
            files={files}
            onDownload={handleFileDownload}
            onDelete={handleFileDelete}
            isLoading={isLoadingFiles}
          />
        </div>
      </div>
    </DashboardLayout>
  );
}

export default function App() {
  return (
    <ToastProvider>
      <AppContent />
    </ToastProvider>
  );
}
