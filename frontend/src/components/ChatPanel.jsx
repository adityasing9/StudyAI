import { useState, useRef, useEffect } from 'react';
import './ChatPanel.css';

export default function ChatPanel({ messages, onSend, loading, activeDocId }) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  useEffect(() => {
    setInput('');
    inputRef.current?.focus();
  }, [activeDocId]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;
    onSend(input.trim());
    setInput('');
  };

  if (!activeDocId) {
    return (
      <div className="chat-empty-state">
        <div className="empty-card">
          <span className="empty-emoji">📚</span>
          <h2>Welcome to StudyAI</h2>
          <p>Upload a document and select it from the sidebar to start chatting with your study materials.</p>
          <div className="empty-features">
            <div className="feature-pill"><span>💬</span> Ask Questions</div>
            <div className="feature-pill"><span>📊</span> Get Summaries</div>
            <div className="feature-pill"><span>🎯</span> Practice Exams</div>
            <div className="feature-pill"><span>📌</span> Source Proofs</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-panel">
      <div className="chat-messages">
        {messages.length === 0 && !loading && (
          <div className="chat-start-hint">
            <span>💡</span>
            <p>Start by asking a question about your document</p>
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`} style={{ animationDelay: `${i * 0.05}s` }}>
            <div className="message-avatar">
              {msg.role === 'user' ? '👤' : '🧠'}
            </div>
            <div className="message-content">
              <div className="message-bubble">
                <p className="message-text">{msg.content}</p>
              </div>
              {msg.role === 'ai' && msg.confusion_detected && (
                <div className="confusion-badge">
                  <span>🔄</span> Adaptive mode activated — simplified explanation
                </div>
              )}
              {msg.role === 'ai' && msg.sources && msg.sources.length > 0 && (
                <div className="source-section">
                  <div className="source-header">
                    <span className="source-icon">📌</span>
                    <span className="source-label">Source from document</span>
                  </div>
                  <div className="source-chunks">
                    {msg.sources.map((src, j) => (
                      <div key={j} className="source-chunk">
                        <div className="chunk-indicator">Chunk {j + 1}</div>
                        <p className="chunk-text">{src}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message ai loading-msg">
            <div className="message-avatar">🧠</div>
            <div className="message-content">
              <div className="message-bubble loading-bubble">
                <div className="typing-indicator">
                  <span></span><span></span><span></span>
                </div>
                <p className="loading-text">Analyzing document…</p>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <div className="input-wrapper">
          <input
            ref={inputRef}
            type="text"
            className="chat-input"
            placeholder="Ask a question about your document…"
            value={input}
            onChange={e => setInput(e.target.value)}
            disabled={loading}
          />
          <button type="submit" className="send-btn" disabled={!input.trim() || loading}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" />
            </svg>
          </button>
        </div>
      </form>
    </div>
  );
}
