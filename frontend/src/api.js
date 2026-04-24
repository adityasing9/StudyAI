const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000/api';

export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: formData });
  if (!res.ok) { const err = await res.json(); throw new Error(err.detail || 'Upload failed'); }
  return res.json();
}

export async function getDocuments() {
  const res = await fetch(`${API_BASE}/documents`);
  if (!res.ok) throw new Error('Failed to fetch documents');
  return res.json();
}

export async function deleteDocument(id) {
  const res = await fetch(`${API_BASE}/documents/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete document');
  return res.json();
}

export async function chatWithDocument(documentId, question, explainLevel, adaptiveMode) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ document_id: documentId, question, explain_level: explainLevel, adaptive_mode: adaptiveMode }),
  });
  if (!res.ok) { const err = await res.json(); throw new Error(err.detail || 'Chat failed'); }
  return res.json();
}

export async function getChatHistory(documentId) {
  const res = await fetch(`${API_BASE}/chat/history/${documentId}`);
  if (!res.ok) throw new Error('Failed to fetch chat history');
  return res.json();
}

export async function generateSummary(documentId) {
  const res = await fetch(`${API_BASE}/summary`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ document_id: documentId }),
  });
  if (!res.ok) { const err = await res.json(); throw new Error(err.detail || 'Summary failed'); }
  return res.json();
}

export async function generateExam(documentId) {
  const res = await fetch(`${API_BASE}/exam`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ document_id: documentId }),
  });
  if (!res.ok) { const err = await res.json(); throw new Error(err.detail || 'Exam generation failed'); }
  return res.json();
}
