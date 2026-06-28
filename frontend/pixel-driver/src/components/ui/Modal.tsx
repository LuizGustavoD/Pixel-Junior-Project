import React, { useEffect, useState } from 'react';
import './Modal.css';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'fit';
  draggable?: boolean;
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
  draggable = false,
}) => {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  // Reset position when modal opens/closes
  useEffect(() => {
    if (!isOpen) {
      setPosition({ x: 0, y: 0 });
    }
  }, [isOpen]);

  // Prevent body scrolling when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  // Mouse move and up handlers for dragging
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      setPosition({
        x: e.clientX - dragStart.x,
        y: e.clientY - dragStart.y,
      });
    };

    const handleMouseUp = () => {
      setIsDragging(false);
    };

    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, dragStart]);

  if (!isOpen) return null;

  const handleMouseDown = (e: React.MouseEvent) => {
    if (!draggable) return;
    if (e.button !== 0) return; // Left click only
    if ((e.target as HTMLElement).closest('.modal-close')) return; // Ignore close button click

    e.preventDefault();
    setIsDragging(true);
    setDragStart({
      x: e.clientX - position.x,
      y: e.clientY - position.y,
    });
  };

  const containerStyle: React.CSSProperties = {};
  if (position.x !== 0 || position.y !== 0) {
    containerStyle.transform = `translate(${position.x}px, ${position.y}px)`;
  }
  if (isDragging) {
    containerStyle.cursor = 'grabbing';
    containerStyle.transition = 'none'; // Disable transition during drag for smoothness
  }

  const headerStyle: React.CSSProperties = {};
  if (draggable) {
    headerStyle.cursor = isDragging ? 'grabbing' : 'grab';
    headerStyle.userSelect = 'none'; // Prevent text selection in header while dragging
  }

  return (
    <div className="modal-backdrop animate-fade-in" onClick={onClose}>
      <div
        className={`modal-draggable-wrapper modal-size-${size}`}
        style={containerStyle}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-container">
          <div
            className="modal-header"
            style={headerStyle}
            onMouseDown={handleMouseDown}
          >
            {title && <h3 className="modal-title">{title}</h3>}
            <button className="modal-close" onClick={onClose} aria-label="Fechar">
              ×
            </button>
          </div>
          <div className="modal-body">{children}</div>
        </div>
      </div>
    </div>
  );
};
