import React, { useState } from 'react';
import { Input } from './ui/Input';
import { Button } from './ui/Button';
import { loginUser } from '../services/auth';
import { useToast } from './ui/Toast';
import { TOKEN_STORAGE_KEY } from '../constants/api';
import './AuthForm.css';

interface LoginFormProps {
  onSuccess: (token: string) => void;
  onToggleForm: () => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSuccess, onToggleForm }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});
  const [isLoading, setIsLoading] = useState(false);
  const { showToast } = useToast();

  const validate = () => {
    const tempErrors: typeof errors = {};
    if (!email) {
      tempErrors.email = 'E-mail é obrigatório';
    } else if (!email.includes('@') || !email.includes('.')) {
      tempErrors.email = 'E-mail com formato inválido';
    }

    if (!password) {
      tempErrors.password = 'Senha é obrigatória';
    }

    setErrors(tempErrors);
    return Object.keys(tempErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    try {
      const response = await loginUser(email, password);
      localStorage.setItem(TOKEN_STORAGE_KEY, response.access_token);
      showToast('Login realizado com sucesso!', 'success');
      onSuccess(response.access_token);
    } catch (err: any) {
      showToast(err.message || 'Erro ao realizar login.', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form className="auth-form animate-fade-in" onSubmit={handleSubmit}>
      <h2 className="auth-title">Entrar na sua conta</h2>
      <p className="auth-subtitle">Gerencie e envie seus arquivos com segurança</p>

      <Input
        label="E-mail"
        type="email"
        placeholder="exemplo@pixel.com"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        error={errors.email}
        disabled={isLoading}
      />

      <Input
        label="Senha"
        type="password"
        placeholder="Sua senha secreta"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        error={errors.password}
        disabled={isLoading}
      />

      <Button type="submit" variant="primary" isLoading={isLoading} className="auth-submit-btn">
        Entrar
      </Button>

      <div className="auth-toggle-container">
        <span>Não tem uma conta?</span>
        <button type="button" className="auth-toggle-btn" onClick={onToggleForm} disabled={isLoading}>
          Criar conta
        </button>
      </div>
    </form>
  );
};
