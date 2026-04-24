import { useState, useRef } from 'react';
import './Sidebar.css';

export default function Sidebar({ documents, activeDocId, onSelectDoc, onDeleteDoc, onUpload, uploading }) {
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) { onUpload(file); e.target.value = ''; }
  };

  const getFileIcon = (type) => type === 'pdf' ? '📄' : '📝';

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <span className="logo-icon">🧠</span>
          <h1 className="logo-text">StudyAI</h1>
        </div>
        <p className="logo-sub">Mini NotebookLM</p>
      </div>

      <div className="sidebar-upload">
        <button className="upload-btn" onClick={() => fileInputRef.current?.click()} disabled={uploading}>
          {uploading ? (
            <><span className="spinner" /> Uploading...</>
          ) : (
            <><span className="upload-icon">+</span> Upload Document</>
          )}
        </button>
        <input ref={fileInputRef} type="file" accept=".pdf,.txt" onChange={handleFileSelect} hidden />
      </div>

      <div className="sidebar-docs">
        <p className="docs-label">Your Documents</p>
        {documents.length === 0 ? (
          <div className="docs-empty">
            <span className="empty-icon">📂</span>
            <p>No documents yet</p>
            <p className="empty-sub">Upload a PDF or TXT to begin</p>
          </div>
        ) : (
          <ul className="docs-list">
            {documents.map(doc => (
              <li key={doc.id} className={`doc-item ${activeDocId === doc.id ? 'active' : ''}`} onClick={() => onSelectDoc(doc.id)}>
                <span className="doc-icon">{getFileIcon(doc.file_type)}</span>
                <div className="doc-info">
                  <span className="doc-name">{doc.name}</span>
                  <span className="doc-meta">{doc.chunk_count} chunks · {doc.file_type.toUpperCase()}</span>
                </div>
                <button className="doc-delete" onClick={(e) => { e.stopPropagation(); onDeleteDoc(doc.id); }} title="Delete">×</button>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="sidebar-footer">
        <p>Built with ❤️ &amp; RAG</p>
      </div>
    </aside>
  );
}
