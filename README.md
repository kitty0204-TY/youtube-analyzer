# 🐍 Java-Python MSA 기반 비디오 콘텐츠 분석 엔진

## 🌟 프로젝트 개요
YouTube 영상 URL을 입력받아 한국어 자막을 추출하고, Python의 Flask 서버에서 감성 분석 및 키워드 추출을 수행하는 **마이크로서비스 아키텍처(MSA)** 실습 프로젝트입니다. **Java (Spring Boot) 서버**를 게이트웨이로 사용하여 **Python (Flask) 서버**와 통신하는 이종 언어 연동 구조를 성공적으로 구현했습니다.

## 🛠️ 주요 기술 스택

| Category | Technology | Description |
| :--- | :--- | :--- |
| **Gateway/Client** | ![Java](https://img.shields.io/badge/Java-007396?style=flat-square&logo=OpenJDK&logoColor=white) ![Spring Boot](https://img.shields.io/badge/SpringBoot-6DB33F?style=flat-square&logo=spring-boot&logoColor=white) | 외부 요청 처리 및 Python 마이크로서비스 호출 (REST API) |
| **Microservice** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) | AI 분석 전담. 자막 추출, 감성 분석, 키워드 추출 로직 실행 |
| **API** | `youtube-transcript-api` | 비디오 ID 기반 자막 데이터 추출 |
| **Data Format** | JSON | Java와 Python 간 데이터 직렬화 및 역직렬화 통신 규약 |

## 🏗️ 아키텍처 및 시스템 설계 (MSA 구조 강조)

이 프로젝트는 다음과 같은 2개의 독립된 서비스로 구성됩니다.

### 1. Spring Boot Gateway (Port 8080)
* **역할:** 사용자(React) 요청을 받아서 Python 서비스로 전달(라우팅)하고, Python의 결과를 받아 사용자에게 최종 응답을 반환합니다.
* **핵심 구현:** `RestTemplate` 또는 `WebClient`를 이용한 **외부 HTTP 요청 처리** 및 JSON 응답 데이터 파싱.

### 2. Python Microservice (Port 5000)
* **역할:** Java 서버로부터 받은 URL을 처리하고, 모든 분석 작업을 수행합니다.
* **핵심 구현:** Flask를 사용하여 경량 API를 구축하고, YouTube Transcript API를 활용해 데이터를 수집합니다.

## ✨ 주요 구현 기능

| 기능 | 상세 설명 | 기술적 의의 |
| :--- | :--- | :--- |
| **MSA 구현** | Java/Python 서버를 분리하여 운영, 서비스 간 독립적인 개발/배포 가능성 확보 | **이종 언어 연동** 경험 및 서비스 경계 설정 능력 어필 |
| **감성 분석** | (Okt 제외) 키워드 딕셔너리 기반의 긍정/부정 스코어링 로직 구현 | 비즈니스 로직에 기반한 데이터 분석 알고리즘 적용 |
| **자막 추출** | URL에서 Video ID 추출 후, 한국어 자막이 존재하면 전체 텍스트 수집 | 외부 API 연동 및 예외 처리 (자막 없는 경우) |

## ⚙️ 실행 방법

### 1. Python 환경 설정 (Microservice)
1.  Python 3.11 버전에서 `pip install flask youtube-transcript-api` 실행
2.  `youtube-analyzer` 폴더에서 `python app.py`를 실행하여 5000번 포트에 서버를 켜둡니다.

### 2. Java 환경 설정 (Gateway)
1.  IntelliJ IDEA에서 프로젝트를 열고, `YoutubeService.java` 파일의 Python API 주소를 확인합니다 (`http://127.0.0.1:5000` 또는 `http://localhost:5000`).
2.  메인 클래스를 실행하여 8080 포트에 Java 서버를 킵니다.

### 3. 테스트 (React or Postman)
* 프론트엔드(React) 환경에서 실행하거나, Postman을 사용하여 `http://localhost:8080/api/youtube/analyze` 경로로 POST 요청을 보내 분석을 테스트합니다.
