import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const analyzeVideo = async () => {
    if (!url) return;
    setLoading(true);
    setError('');
    setResult(null);

    try {
      // 자바 서버(8080)에게 요청
      const response = await axios.post('http://localhost:8080/api/youtube/analyze', { url });
      setResult(response.data);
    } catch (err) {
      setError('분석 실패! 자막이 없거나 서버 에러입니다.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '50px', maxWidth: '800px', margin: '0 auto', textAlign: 'center' }}>
      <h1>📺 유튜브 AI 분석기</h1>
      
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <input 
          type="text" 
          placeholder="유튜브 링크를 붙여넣으세요 (예: https://youtu.be/...)" 
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{ flex: 1, padding: '10px', fontSize: '16px' }}
        />
        <button onClick={analyzeVideo} disabled={loading} style={{ padding: '10px 20px', cursor: 'pointer' }}>
          {loading ? '분석 중...' : '분석하기'}
        </button>
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {result && (
        <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '10px', textAlign: 'left', backgroundColor: '#f9f9f9' }}>
          <h2>📊 분석 결과</h2>
          <p><strong>감정:</strong> {result.sentiment} ({result.score}점)</p>
          
          <h3>🔑 핵심 키워드</h3>
          <ul>
            {result.keywords.map((kw, index) => (
              <li key={index}>{kw[0]} ({kw[1]}회 등장)</li>
            ))}
          </ul>

          <h3>📝 3줄 요약 (미리보기)</h3>
          <p style={{ color: '#555', lineHeight: '1.6' }}>{result.summary_preview}</p>
        </div>
      )}
    </div>
  );
}

export default App;