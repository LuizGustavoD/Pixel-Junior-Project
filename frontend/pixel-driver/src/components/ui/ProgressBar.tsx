import React from 'react';
import './ProgressBar.css';

interface ProgressBarProps {
  progress: number;
  status?: 'idle' | 'uploading' | 'success' | 'error';
  showText?: boolean;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  status = 'uploading',
  showText = true,
}) => {
  const percentage = Math.min(100, Math.max(0, progress));

  const barClass = [
    'progress-bar-fill',
    `progress-status-${status}`
  ].join(' ');

  return (
    <div className="progress-bar-container">
      <div className="progress-bar-track">
        <div
          className={barClass}
          style={{ width: `${percentage}%` }}
        />
      </div>
      {showText && (
        <div className="progress-bar-info">
          <span className="progress-bar-percentage">{percentage}%</span>
          <span className="progress-bar-status-text">
            {status === 'uploading' && 'Enviando...'}
            {status === 'success' && 'Sucesso!'}
            {status === 'error' && 'Erro no envio'}
          </span>
        </div>
      )}
    </div>
  );
};
