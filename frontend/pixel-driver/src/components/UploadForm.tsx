import React, { useState, useRef } from 'react';
import { Card } from './ui/Card';
import { Button } from './ui/Button';
import { ProgressBar } from './ui/ProgressBar';
import { uploadFile } from '../services/files';
import { useToast } from './ui/Toast';
import './UploadForm.css';

interface UploadFormProps {
  onUploadSuccess: () => void;
}

const ALLOWED_EXTENSIONS = ['.png', '.jpg', '.pdf', '.txt'];
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

export const UploadForm: React.FC<UploadFormProps> = ({ onUploadSuccess }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { showToast } = useToast();

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const validateFile = (file: File): boolean => {
    const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(ext)) {
      setErrorMsg(`Tipo de arquivo não permitido. Apenas ${ALLOWED_EXTENSIONS.join(', ')} são aceitos.`);
      showToast('Arquivo inválido.', 'error');
      return false;
    }

    if (file.size > MAX_FILE_SIZE) {
      setErrorMsg('O arquivo excede o limite máximo de 10MB.');
      showToast('Arquivo muito grande.', 'error');
      return false;
    }

    setErrorMsg(null);
    return true;
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (validateFile(file)) {
        setSelectedFile(file);
        setUploadStatus('idle');
        setUploadProgress(0);
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (validateFile(file)) {
        setSelectedFile(file);
        setUploadStatus('idle');
        setUploadProgress(0);
      }
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploadStatus('uploading');
    setUploadProgress(0);

    try {
      await uploadFile(selectedFile, (progress) => {
        setUploadProgress(progress);
      });
      setUploadStatus('success');
      showToast('Arquivo enviado com sucesso!', 'success');
      setTimeout(() => {
        setSelectedFile(null);
        setUploadStatus('idle');
        setUploadProgress(0);
        onUploadSuccess();
      }, 1500);
    } catch (err: any) {
      setUploadStatus('error');
      setErrorMsg(err.message || 'Falha ao fazer upload.');
      showToast(err.message || 'Erro ao enviar arquivo.', 'error');
    }
  };

  const clearSelection = () => {
    if (uploadStatus === 'uploading') return;
    setSelectedFile(null);
    setErrorMsg(null);
    setUploadStatus('idle');
    setUploadProgress(0);
  };

  const formatSize = (bytes: number) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <Card className="upload-card">
      <h3 className="upload-card-title">Enviar Arquivo</h3>
      <p className="upload-card-subtitle">
        Envie documentos ou imagens de até 10MB nos formatos PDF, TXT, PNG ou JPG.
      </p>

      {!selectedFile && (
        <div
          className={`dropzone ${dragActive ? 'dropzone-active' : ''}`}
          onDragEnter={handleDrag}
          onDragOver={handleDrag}
          onDragLeave={handleDrag}
          onDrop={handleDrop}
          onClick={triggerFileInput}
        >
          <input
            type="file"
            ref={fileInputRef}
            className="file-input-hidden"
            onChange={handleFileChange}
            accept=".png,.jpg,.jpeg,.pdf,.txt"
          />
          <div className="dropzone-icon">
            <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5a4.5 4.5 0 01-1.41-8.775 5.25 5.25 0 0110.233-2.33 3 3 0 013.758 3.848A3.752 3.752 0 0118 19.5H6.75z" />
            </svg>
          </div>
          <p className="dropzone-text">
            Arraste seu arquivo para cá ou <span className="dropzone-browse">procure no computador</span>
          </p>
        </div>
      )}

      {selectedFile && (
        <div className="file-preview-container animate-fade-in">
          <div className="file-preview-header">
            <div className="file-preview-details">
              <span className="file-preview-name">{selectedFile.name}</span>
              <span className="file-preview-size">{formatSize(selectedFile.size)}</span>
            </div>
            <button
              className="file-preview-remove"
              onClick={clearSelection}
              disabled={uploadStatus === 'uploading'}
              title="Remover arquivo"
            >
              ×
            </button>
          </div>

          {uploadStatus !== 'idle' && (
            <div className="upload-progress-box">
              <ProgressBar progress={uploadProgress} status={uploadStatus} />
            </div>
          )}

          {errorMsg && <div className="upload-error-msg">{errorMsg}</div>}

          {uploadStatus !== 'success' && uploadStatus !== 'uploading' && (
            <Button className="upload-start-btn" variant="primary" onClick={handleUpload}>
              Iniciar Upload
            </Button>
          )}
        </div>
      )}
    </Card>
  );
};
