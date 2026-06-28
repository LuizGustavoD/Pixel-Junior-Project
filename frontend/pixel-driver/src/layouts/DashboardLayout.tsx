import React from 'react';
import logoImg from '../assets/images/pixelBreedersPurple-DIGct69i.svg';
import { Button } from '../components/ui/Button';
import type { User } from '../types';
import './DashboardLayout.css';

interface DashboardLayoutProps {
  children: React.ReactNode;
  user: User | null;
  onLogout: () => void;
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  children,
  user,
  onLogout,
}) => {
  return (
    <div className="dashboard-layout">
      <header className="dashboard-header glassmorphism">
        <div className="header-container">
          <div className="header-logo">
            <img src={logoImg} alt="PixelBreeders Logo" height="38" className="logo-img" />
          </div>
          
          <div className="header-user-menu">
            <div className="user-profile-info">
              <div className="user-avatar">
                {user?.username ? user.username.charAt(0).toUpperCase() : 'U'}
              </div>
              <div className="user-text">
                <span className="user-name">{user?.username || 'Usuário'}</span>
                <span className="user-email">{user?.email || ''}</span>
              </div>
            </div>
            
            <Button variant="secondary" size="sm" onClick={onLogout} className="logout-btn">
              Sair
            </Button>
          </div>
        </div>
      </header>
      
      <main className="dashboard-main-content">
        <div className="main-container">
          {children}
        </div>
      </main>
    </div>
  );
};
