import './TopBar.css';

export default function TopBar({ activeDoc, explainLevel, setExplainLevel, adaptiveMode, setAdaptiveMode, onSummarize, onExam, loading }) {
  return (
    <header className="topbar">
      <div className="topbar-left">
        {activeDoc ? (
          <div className="topbar-doc-info">
            <span className="topbar-doc-icon">{activeDoc.file_type === 'pdf' ? '📄' : '📝'}</span>
            <div>
              <h2 className="topbar-doc-name">{activeDoc.name}</h2>
              <span className="topbar-doc-meta">{activeDoc.chunk_count} chunks · {activeDoc.file_type.toUpperCase()}</span>
            </div>
          </div>
        ) : (
          <h2 className="topbar-title">Select a document to begin</h2>
        )}
      </div>

      <div className="topbar-actions">
        <button className="action-btn summary-btn" onClick={onSummarize} disabled={!activeDoc || loading} title="Summarize Document">
          <span>📊</span> Summarize
        </button>

        <button className="action-btn exam-btn" onClick={onExam} disabled={!activeDoc || loading} title="Generate Exam Questions">
          <span>🎯</span> Exam Mode
        </button>

        <div className="topbar-divider" />

        <div className="topbar-control">
          <label className="control-label">Explain Level</label>
          <select className="control-select" value={explainLevel} onChange={e => setExplainLevel(e.target.value)} disabled={!activeDoc}>
            <option value="beginner">🟢 Beginner</option>
            <option value="intermediate">🟡 Intermediate</option>
            <option value="expert">🔴 Expert</option>
          </select>
        </div>

        <div className="topbar-control adaptive-control">
          <label className="control-label">Adaptive AI</label>
          <button className={`toggle-btn ${adaptiveMode ? 'active' : ''}`} onClick={() => setAdaptiveMode(!adaptiveMode)} disabled={!activeDoc}>
            <span className="toggle-track"><span className="toggle-thumb" /></span>
            <span className="toggle-label">{adaptiveMode ? 'ON' : 'OFF'}</span>
          </button>
        </div>
      </div>
    </header>
  );
}
