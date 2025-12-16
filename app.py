from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from collections import Counter
import re

app = Flask(__name__)

# Okt 관련 코드는 전부 삭제되었습니다!

def extract_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    return match.group(1) if match else None

def calculate_sentiment(text):
    # 간단 긍정/부정 사전
    pos_words = ['좋다', '최고', '추천', '유익', '대박', '성공', '사랑', '감사', '재밌다', '꿀팁', '도움', '성장']
    neg_words = ['별로', '실망', '최악', '노잼', '반대', '실패', '환불', '쓰레기', '비추', '문제', '어려움']
    
    score = 0
    # 텍스트 전체에서 단어 개수 세기
    for word in pos_words:
        score += text.count(word)
    for word in neg_words:
        score -= text.count(word)
        
    if score > 0: return "긍정적", min(score * 10, 100)
    elif score < 0: return "부정적", max(score * 10, -100)
    else: return "중립", 50

@app.route('/', methods=['POST'])
def analyze_youtube():
    try:
        data = request.get_json()
        video_url = data.get('url')
        print(f"요청 받음: {video_url}")

        if not video_url: return jsonify({"status": "error", "message": "URL 없음"}), 400

        video_id = extract_video_id(video_url)
        if not video_id: return jsonify({"status": "error", "message": "URL 이상함"}), 400
        
        # 자막 가져오기
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
        except:
            return jsonify({"status": "error", "message": "한국어 자막 없음"}), 404
        
        full_text = " ".join([t['text'] for t in transcript_list])

        # Okt 대신 띄어쓰기 기준으로 단어 나누고 2글자 이상만 추출
        words = [w for w in full_text.split() if len(w) >= 2]
        count = Counter(words)
        top_keywords = count.most_common(5)

        sentiment, score = calculate_sentiment(full_text)

        result = {
            "status": "success",
            "video_id": video_id,
            "sentiment": sentiment,
            "score": score,
            "keywords": top_keywords,
            "summary_preview": full_text[:100] + "..." 
        }
        
        return jsonify(result)

    except Exception as e:
        print(f"에러: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000) #