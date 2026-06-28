import React, { useState } from 'react';
import { Input } from './ui/Input';
import { Button } from './ui/Button';
import { registerUser } from '../services/auth';
import { useToast } from './ui/Toast';
import './AuthForm.css';

interface RegisterFormProps {
  onSuccess: () => void;
  onToggleForm: () => void;
}

export const RegisterForm: React.FC<RegisterFormProps> = ({ onSuccess, onToggleForm }) => {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{ email?: string; username?: string; password?: string }>({});
  const [isLoading, setIsLoading] = useState(false);
  const { showToast } = useToast();

  const validate = () => {
    const tempErrors: typeof errors = {};
    if (!email) {
      tempErrors.email = 'E-mail é obrigatório';
    } else if (!email.includes('@') || !email.includes('.')) {
      tempErrors.email = 'E-mail com formato inválido';
    }

    if (!username) {
      tempErrors.username = 'Nome de usuário é obrigatório';
    } else if (username.length < 3) {
      tempErrors.username = 'Nome de usuário deve conter pelo menos 3 caracteres';
    }

    if (!password) {
      tempErrors.password = 'Senha é obrigatória';
    } else if (password.length < 6) {
      tempErrors.password = 'A senha deve conter pelo menos 6 caracteres';
    }

    setErrors(tempErrors);
    return Object.keys(tempErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    try {
      await registerUser(email, username, password);
      showToast('Conta criada com sucesso! Faça login para continuar.', 'success');
      onSuccess();
    } catch (err: any) {
      showToast(err.message || 'Erro ao realizar cadastro.', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form className="auth-form animate-fade-in" onSubmit={handleSubmit}>
      <h2 className="auth-title">Criar uma nova conta</h2>
      <p className="auth-subtitle">Junte-se à plataforma Pixel e organize seus arquivos</p>

      <Input
        label="Nome de Usuário"
        type="text"
        placeholder="Seu apelido ou nome"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        error={errors.username}
        disabled={isLoading}
      />

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
        placeholder="Mínimo 6 caracteres"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        error={errors.password}
        disabled={isLoading}
      />

      <Button type="submit" variant="primary" isLoading={isLoading} className="auth-submit-btn">
        Cadastrar
      </Button>

      <div className="auth-toggle-container">
        <span>Já tem uma conta?</span>
        <button type="button" className="auth-toggle-btn" onClick={onToggleForm} disabled={isLoading}>
          Entrar
        </button>
      </div>
    </form>
  );
};
