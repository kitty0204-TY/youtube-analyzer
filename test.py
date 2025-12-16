import requests
import json

# 자바 서버(8080)로 요청 보낼 주소
url = "http://localhost:8080/api/youtube/analyze"

# [수정] 황석희 번역가 세바시 강연 (자막 100% 있음!)
data = {"url": "https://www.youtube.com/watch?v=h71OyCt8-Z8"} 

print("📨 자바 서버(사장님)에게 요청 보내는 중...")
try:
    response = requests.post(url, json=data)
    
    print(f"응답 코드: {response.status_code}")
    print("✅ 자바가 받아온 결과:")
    # 결과 예쁘게 출력
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    
except Exception as e:
    print(f"❌ 에러 발생: {e}")