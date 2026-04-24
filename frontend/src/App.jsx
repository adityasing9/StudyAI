import { useState, useEffect, useCallback } from 'react';
import Sidebar from './components/Sidebar';
import TopBar from './components/TopBar';
import ChatPanel from './components/ChatPanel';
import ResultModal from './components/ResultModal';
import { getDocuments, uploadDocument, deleteDocument, chatWithDocument, getChatHistory, generateSummary, generateExam } from './api';
import './App.css';

export default function App() {
  const [documents, setDocuments] = useState([]);
  const [activeDocId, setActiveDocId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [explainLevel, setExplainLevel] = useState('intermediate');
  const [adaptiveMode, setAdaptiveMode] = useState(false);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [modalData, setModalData] = useState(null);
  const [modalType, setModalType] = useState(null);

  const activeDoc = documents.find(d => d.id === activeDocId) || null;

  // Fetch documents on mount
  useEffect(() => {
    fetchDocuments();
  }, []);

  // Load chat history when switching documents
  useEffect(() => {
    if (activeDocId) {
      loadChatHistory(activeDocId);
    } else {
      setMessages([]);
    }
  }, [activeDocId]);

  const fetchDocuments = async () => {
    try {
      const docs = await getDocuments();
      setDocuments(docs);
    } catch (err) {
      console.error('Failed to fetch documents:', err);
    }
  };

  const loadChatHistory = async (docId) => {
    try {
      const history = await getChatHistory(docId);
      const msgs = [];
      history.forEach(chat => {
        msgs.push({ role: 'user', content: chat.question });
        msgs.push({ role: 'ai', content: chat.answer, sources: [] });
      });
      setMessages(msgs);
    } catch (err) {
      console.error('Failed to load chat history:', err);
      setMessages([]);
    }
  };

  const handleUpload = async (file) => {
    setUploading(true);
    try {
      const result = await uploadDocument(file);
      await fetchDocuments();
      setActiveDocId(result.id);
    } catch (err) {
      alert('Upload failed: ' + err.message);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (docId) => {
    if (!confirm('Delete this document?')) return;
    try {
      await deleteDocument(docId);
      if (activeDocId === docId) {
        setActiveDocId(null);
        setMessages([]);
      }
      await fetchDocuments();
    } catch (err) {
      alert('Delete failed: ' + err.message);
    }
  };

  const handleSend = async (question) => {
    if (!activeDocId) return;
    setMessages(prev => [...prev, { role: 'user', content: question }]);
    setLoading(true);

    try {
      const result = await chatWithDocument(activeDocId, question, explainLevel, adaptiveMode);
      setMessages(prev => [
        ...prev,
        {
          role: 'ai',
          content: result.answer,
          sources: result.sources || [],
          confusion_detected: result.confusion_detected,
        },
      ]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: 'ai', content: 'Sorry, an error occurred: ' + err.message, sources: [] },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSummarize = async () => {
    if (!activeDocId) return;
    setLoading(true);
    try {
      const result = await generateSummary(activeDocId);
      setModalType('summary');
      setModalData(result);
    } catch (err) {
      alert('Summary failed: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExam = async () => {
    if (!activeDocId) return;
    setLoading(true);
    try {
      const result = await generateExam(activeDocId);
      setModalType('exam');
      setModalData(result);
    } catch (err) {
      alert('Exam generation failed: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const closeModal = () => {
    setModalData(null);
    setModalType(null);
  };

  return (
    <div className="app-layout">
      <Sidebar
        documents={documents}
        activeDocId={activeDocId}
        onSelectDoc={setActiveDocId}
        onDeleteDoc={handleDelete}
        onUpload={handleUpload}
        uploading={uploading}
      />
      <div className="app-main">
        <TopBar
          activeDoc={activeDoc}
          explainLevel={explainLevel}
          setExplainLevel={setExplainLevel}
          adaptiveMode={adaptiveMode}
          setAdaptiveMode={setAdaptiveMode}
          onSummarize={handleSummarize}
          onExam={handleExam}
          loading={loading}
        />
        <div className="app-content">
          <ChatPanel
            messages={messages}
            onSend={handleSend}
            loading={loading}
            activeDocId={activeDocId}
          />
        </div>
      </div>

      {modalData && (
        <ResultModal type={modalType} data={modalData} onClose={closeModal} />
      )}
    </div>
  );
}
