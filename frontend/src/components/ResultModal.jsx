import './ResultModal.css';

export default function ResultModal({ type, data, onClose }) {
  if (!data) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-container" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title-row">
            <span className="modal-icon">{type === 'summary' ? '📊' : '🎯'}</span>
            <h2>{type === 'summary' ? 'Document Summary' : 'Exam Questions'}</h2>
          </div>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          {type === 'summary' && data.summary && (
            <div className="summary-content">
              <div className="summary-card highlight-card">
                <h3>📝 One-Line Summary</h3>
                <p className="one-line">{data.summary.one_line}</p>
              </div>

              <div className="summary-card">
                <h3>📋 Key Points</h3>
                <ul className="bullet-list">
                  {(data.summary.bullet_points || []).map((point, i) => (
                    <li key={i}><span className="bullet-num">{i + 1}</span>{point}</li>
                  ))}
                </ul>
              </div>

              <div className="summary-card">
                <h3>📖 Detailed Explanation</h3>
                <p className="detailed-text">{data.summary.detailed}</p>
              </div>
            </div>
          )}

          {type === 'exam' && data.exam && (
            <div className="exam-content">
              {data.exam.mcqs && data.exam.mcqs.length > 0 && (
                <div className="exam-section">
                  <h3 className="section-title">📝 Multiple Choice Questions</h3>
                  {data.exam.mcqs.map((q, i) => (
                    <McqCard key={i} question={q} index={i} />
                  ))}
                </div>
              )}

              {data.exam.short_answers && data.exam.short_answers.length > 0 && (
                <div className="exam-section">
                  <h3 className="section-title">✍️ Short Answer Questions</h3>
                  {data.exam.short_answers.map((q, i) => (
                    <ShortAnswerCard key={i} question={q} index={i} />
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function McqCard({ question, index }) {
  return (
    <div className="mcq-card" style={{ animationDelay: `${index * 0.08}s` }}>
      <div className="mcq-header">
        <span className="q-num">Q{index + 1}</span>
        <p className="q-text">{question.question}</p>
      </div>
      <div className="mcq-options">
        {(question.options || []).map((opt, j) => (
          <div key={j} className={`mcq-option ${opt.startsWith(question.correct) ? 'correct' : ''}`}>
            {opt}
            {opt.startsWith(question.correct) && <span className="correct-badge">✓ Correct</span>}
          </div>
        ))}
      </div>
      {question.explanation && (
        <div className="mcq-explanation">
          <strong>Explanation:</strong> {question.explanation}
        </div>
      )}
    </div>
  );
}

function ShortAnswerCard({ question, index }) {
  return (
    <div className="sa-card" style={{ animationDelay: `${index * 0.08}s` }}>
      <div className="sa-header">
        <span className="q-num">Q{index + 1}</span>
        <p className="q-text">{question.question}</p>
      </div>
      <div className="sa-answer">
        <strong>Answer:</strong> {question.answer}
      </div>
    </div>
  );
}
