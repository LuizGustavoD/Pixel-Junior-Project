export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

export function formatDate(isoString: string): string {
  try {
    if (!isoString) return '-';
    let parsedString = isoString.replace(' ', 'T');
    if (!parsedString.endsWith('Z') && !parsedString.includes('+') && !/-\d{2}:\d{2}$/.test(parsedString)) {
      parsedString = parsedString + 'Z';
    }
    const date = new Date(parsedString);
    if (isNaN(date.getTime())) return '-';
    
    return date.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return '-';
  }
}
