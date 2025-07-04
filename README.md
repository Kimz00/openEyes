# 🚗 AI 졸음 예측 및 경고 시스템

> 운전자의 눈 깜빡임 패턴을 실시간으로 분석하고, 졸음 상태를 예측해 일정 시간 이상 감김 상태가 지속될 경우 음성 경고를 제공하는 Python 기반 웹 애플리케이션입니다.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-green?logo=flask)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📸 데모 스크린샷


---

## 🚀 주요 기능

✅ **실시간 EAR 계산**  
✅ **Mediapipe 얼굴/눈 검출**  
✅ **졸음 상태(주의/위험) 자동 분류**  
✅ **OS별 음성 경고 출력**  
✅ **웹 대시보드 시각화**

---

## 📂 디렉토리 구조

```text
openEyes/
├── app.py                 # Flask 서버 애플리케이션
├── ear_utils.py           # EAR 계산 유틸리티
├── face_eye_detection.py  # Mediapipe 얼굴/눈 검출 함수
├── text_utils.py          # 이미지에 한글 출력 함수
├── requirements.txt       # 패키지 목록
├── templates/
│   └── index.html         # 메인 웹페이지
├── static/
│   └── script.js          # UI 및 데이터 업데이트 스크립트
└── README.md

```


---

<pre> ```text 🖥️ 주요 파일 설명 app.py - Flask 서버 - EAR 값 업데이트 백그라운드 스레드 - 상태 API (/ear) 제공 - 음성 경고 처리 ear_utils.py - Eye Aspect Ratio(EAR) 계산 함수 - 눈의 좌표를 입력받아 EAR 반환 face_eye_detection.py - Mediapipe 얼굴/눈 랜드마크 추출 - 검출된 눈 좌표 반환 text_utils.py - OpenCV 프레임에 한글 텍스트 표시 (Pillow) templates/index.html - UI 레이아웃 - EAR 값, 상태 표시 - 로그 및 그래프 영역 static/script.js - /ear API를 주기적으로 호출 - UI 실시간 업데이트 - 로그 출력 및 그래프 데이터 처리 ``` </pre>

---

## 🛠️ 설치 및 실행 방법

### 1️⃣ 가상환경 생성

```bash
python -m venv venv
```

---

### 2️⃣ 가상환경 활성화

**macOS/Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```powershell
venv\Scripts\activate
```

---

### 3️⃣ 필수 패키지 설치

```bash
pip install -r requirements.txt
```

---

### 4️⃣ 서버 실행

```bash
python app.py
```

---

### 5️⃣ 웹페이지 접속

```
http://127.0.0.1:
```
---

## 🗣️ 음성 경고 동작
| 운영체제    | 출력 방식                    |
| -------   | ------------------------   |
| macOS     | `say` 커맨드 (Yuna 한국어 음성) |
| Windows   | `pyttsx3` (Heami 한국어 음성) |

### Mac 예제:
```bash
subprocess.run(['say', '-v', 'Yuna', '경고! 졸음 상태가 감지되었습니다.'])
```

### Windows 예제:
```powershell
engine.say("경고! 졸음 상태가 감지되었습니다.")
engine.runAndWait()
```

---

## 🎛️ EAR 기준값 및 로직
• EAR < 0.23 : 위험
• EAR < 0.26 : 주의
• EAR >= 0.26 : 정상
• 위험 상태 3초 이상 지속 시 음성 경고
• 다시 눈을 뜨면 카운트 초기화

---

## 🛠️ 주요 기술 스택
• Python
• Flask
• OpenCV
• Mediapipe
• pyttsx3
• JavaScript

---


