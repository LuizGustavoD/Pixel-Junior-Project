import React, { useState } from 'react';
import { Card } from './ui/Card';
import { Button } from './ui/Button';
import { Modal } from './ui/Modal';
import { getFilePreviewUrl } from '../services/files';
import { useToast } from './ui/Toast';
import type { FileMetadata } from '../types';
import { formatFileSize, formatDate } from '../utils/format';
import './FileList.css';

interface FileListProps {
  files: FileMetadata[];
  onDownload: (fileId: string, filename: string) => Promise<void>;
  onDelete: (fileId: string) => Promise<void>;
  isLoading: boolean;
}

export const FileList: React.FC<FileListProps> = ({
  files,
  onDownload,
  onDelete,
  isLoading,
}) => {
  const [downloadingId, setDownloadingId] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [confirmDeleteId, setConfirmDeleteId] = useState<string | null>(null);
  const [previewingId, setPreviewingId] = useState<string | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [previewFilename, setPreviewFilename] = useState<string | null>(null);
  const { showToast } = useToast();

  const isImageFile = (filename: string, contentType: string) => {
    const ext = filename.substring(filename.lastIndexOf('.')).toLowerCase();
    return ['.png', '.jpg', '.jpeg'].includes(ext) || contentType.startsWith('image/');
  };

  const getFileIcon = (contentType: string, filename: string) => {
    const ext = filename.substring(filename.lastIndexOf('.')).toLowerCase();
    
    // PDF
    if (ext === '.pdf' || contentType.includes('pdf')) {
      return (
        <div className="file-icon file-icon-pdf">
          <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m.75 12l3 3m0 0l3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
          </svg>
        </div>
      );
    }
    
    // Images
    if (isImageFile(filename, contentType)) {
      return (
        <div className="file-icon file-icon-image">
          <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
          </svg>
        </div>
      );
    }

    // Text files
    if (ext === '.txt' || contentType.includes('text')) {
      return (
        <div className="file-icon file-icon-txt">
          <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9zM9 11.25h6m-6 3h6m-6 3h6" />
          </svg>
        </div>
      );
    }

    // Default file
    return (
      <div className="file-icon file-icon-default">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
        </svg>
      </div>
    );
  };

  const handlePreviewClick = async (fileId: string, filename: string) => {
    setPreviewingId(fileId);
    try {
      const url = await getFilePreviewUrl(fileId);
      setPreviewUrl(url);
      setPreviewFilename(filename);
    } catch (err: any) {
      showToast(err.message || 'Erro ao carregar pré-visualização da imagem.', 'error');
    } finally {
      setPreviewingId(null);
    }
  };

  const handleClosePreview = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setPreviewUrl(null);
    setPreviewFilename(null);
  };

  const handleDownloadClick = async (fileId: string, filename: string) => {
    setDownloadingId(fileId);
    try {
      await onDownload(fileId, filename);
    } finally {
      setDownloadingId(null);
    }
  };

  const handleDeleteClick = async (fileId: string) => {
    setDeletingId(fileId);
    try {
      await onDelete(fileId);
      setConfirmDeleteId(null);
    } finally {
      setDeletingId(null);
    }
  };

  if (isLoading) {
    return (
      <Card className="file-list-card flex-center">
        <div className="file-list-loader">
          <svg className="animate-spin" viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="var(--accent)" strokeWidth="3">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          <span>Carregando seus arquivos...</span>
        </div>
      </Card>
    );
  }

  if (files.length === 0) {
    return (
      <Card className="file-list-card flex-center">
        <div className="file-list-empty animate-fade-in">
          <div className="file-list-empty-icon">
            <svg viewBox="0 0 24 24" width="64" height="64" fill="none" stroke="currentColor" strokeWidth="1">
              <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 13.5h3.86a2.25 2.25 0 012.008 1.24l.885 1.77a2.25 2.25 0 002.007 1.24h1.98a2.25 2.25 0 002.007-1.24l.885-1.77a2.25 2.25 0 012.007-1.24h3.86m-18 1.5h18" />
              <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5m16.5 0a1.5 1.5 0 00-1.5-1.5H16.5m-9 0h9M3.75 7.5L3 5.625A1.125 1.125 0 014.125 4.5h15.75c.621 0 1.125.504 1.125 1.125L20.25 7.5m-16.5 0h16.5" />
            </svg>
          </div>
          <h4>Nenhum arquivo encontrado</h4>
          <p>Faça upload de arquivos usando o painel ao lado para começar.</p>
        </div>
      </Card>
    );
  }

  return (
    <Card className="file-list-card animate-fade-in">
      <div className="file-list-header">
        <h3 className="file-list-title">Meus Arquivos</h3>
        <span className="file-list-count">
          {files.length} {files.length === 1 ? 'arquivo' : 'arquivos'}
        </span>
      </div>

      <div className="file-table-container">
        <table className="file-table">
          <thead>
            <tr>
              <th className="th-name">Nome</th>
              <th className="th-size">Tamanho</th>
              <th className="th-date">Upload</th>
              <th className="th-actions">Ações</th>
            </tr>
          </thead>
          <tbody>
            {files.map((file) => {
              const isDownloading = downloadingId === file.id;
              const isDeleting = deletingId === file.id;
              const isConfirming = confirmDeleteId === file.id;
              const isPreviewing = previewingId === file.id;

              return (
                <tr key={file.id} className="file-row">
                  <td className="td-name">
                    <div className="file-info-cell">
                      {getFileIcon(file.content_type, file.original_name)}
                      <span className="file-name" title={file.original_name}>
                        {file.original_name}
                      </span>
                    </div>
                  </td>
                  <td className="td-size">{formatFileSize(file.size)}</td>
                  <td className="td-date">{formatDate(file.created_at)}</td>
                  <td className="td-actions">
                    {isConfirming ? (
                      <div className="delete-confirm-actions">
                        <span className="confirm-text">Deletar?</span>
                        <Button
                          size="sm"
                          variant="danger"
                          isLoading={isDeleting}
                          onClick={() => handleDeleteClick(file.id)}
                        >
                          Sim
                        </Button>
                        <Button
                          size="sm"
                          variant="secondary"
                          disabled={isDeleting}
                          onClick={() => setConfirmDeleteId(null)}
                        >
                          Não
                        </Button>
                      </div>
                    ) : (
                      <div className="file-actions">
                        {isImageFile(file.original_name, file.content_type) && (
                          <Button
                            size="sm"
                            variant="secondary"
                            isLoading={isPreviewing}
                            onClick={() => handlePreviewClick(file.id, file.original_name)}
                            disabled={isDownloading || isDeleting || isConfirming}
                          >
                            Preview
                          </Button>
                        )}
                        <Button
                          size="sm"
                          variant="secondary"
                          isLoading={isDownloading}
                          onClick={() => handleDownloadClick(file.id, file.original_name)}
                          disabled={isDeleting || isConfirming || isPreviewing}
                        >
                          Baixar
                        </Button>
                        <Button
                          size="sm"
                          variant="text"
                          className="btn-delete"
                          onClick={() => setConfirmDeleteId(file.id)}
                          disabled={isDownloading || isDeleting || isPreviewing}
                        >
                          Deletar
                        </Button>
                      </div>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <Modal
        isOpen={!!previewUrl}
        onClose={handleClosePreview}
        title={`Visualizar Imagem — ${previewFilename}`}
        size="lg"
        draggable={true}
      >
        {previewUrl && (
          <div className="preview-modal-content">
            <div className="preview-image-container">
              <img src={previewUrl} alt={previewFilename || 'Preview'} className="preview-image-element animate-fade-in" />
            </div>
            <div className="preview-actions-bar">
              <Button
                variant="primary"
                onClick={() => {
                  if (previewFilename && previewUrl) {
                    const a = document.createElement('a');
                    a.href = previewUrl;
                    a.download = previewFilename;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                  }
                }}
              >
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" style={{ marginRight: '6px' }}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                </svg>
                Baixar Imagem
              </Button>
              <Button
                variant="secondary"
                onClick={handleClosePreview}
              >
                Fechar
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </Card>
  );
};
