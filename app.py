from flask import Flask, render_template, jsonify
import threading
import time
import cv2
import mediapipe as mp
from ear_utils import calculate_ear
from face_eye_detection import get_eye_landmarks
import pyttsx3
import queue
import platform
import subprocess

app = Flask(__name__)

# Mediapipe 세팅
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)

LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]

# EAR 값과 상태 저장
latest_ear = 0.3
last_voice_time = 0
cooldown_seconds = 5
last_risk_start_time = None

# OS 감지
current_os = platform.system()
print(f"Detected OS: {current_os}")

if current_os == "Windows":
    # 윈도우 pyttsx3 세팅
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # 한국어 음성 찾아서 설정 (예: Heami)
    korean_voice = None
    for v in voices:
        if "Korean" in v.name or "Heami" in v.name:
            korean_voice = v.id
            break
    if korean_voice:
        engine.setProperty('voice', korean_voice)
    else:
        print("⚠️ Windows에서 한국어 음성을 찾을 수 없습니다. 영어로 출력됩니다.")
    
    engine.setProperty('rate', 130)
    engine.setProperty('volume', 1.0)

# 음성 엔진 초기화
engine = pyttsx3.init()

# 목소리/속도/볼륨 설정
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 130)
engine.setProperty('volume', 1.0)

# 음성 큐
speech_queue = queue.Queue()

# 음성 전용 스레드
def speech_worker():
    while True:
        text = speech_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()
        
# 음성 스레드 시작
threading.Thread(target=speech_worker, daemon=True).start()

# 음성 출력 함수
def speak_warning():
    if current_os == "Darwin":
        # macOS: say 커맨드 사용
        subprocess.run(['say', '-v', 'Yuna', '경고! 졸음 상태가 감지되었습니다.'])
    elif current_os == "Windows":
        # Windows: pyttsx3 사용
        engine.say("경고! 졸음 상태가 감지되었습니다.")
        engine.runAndWait()
    else:
        print("⚠️ 이 OS에서는 음성 출력이 지원되지 않습니다.")

# EAR 업데이트 스레드
def update_ear():
    global latest_ear
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb_frame)

        if result.multi_face_landmarks:
            for face_landmarks in result.multi_face_landmarks:
                landmarks = face_landmarks.landmark

                left_eye = get_eye_landmarks(landmarks, LEFT_EYE_IDX, w, h)
                right_eye = get_eye_landmarks(landmarks, RIGHT_EYE_IDX, w, h)

                left_ear = calculate_ear(left_eye)
                right_ear = calculate_ear(right_eye)
                avg_ear = (left_ear + right_ear) / 2.0

                latest_ear = round(avg_ear, 2)
        else:
            latest_ear = 0.3

        time.sleep(0.1)

# 백그라운드 스레드 시작
threading.Thread(target=update_ear, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ear")
def ear():
    global last_risk_start_time
    now = time.time()
    status = "정상"
    risk_duration = 0

    if latest_ear <= 0.23:
        status = "위험"
        # 위험 상태 진입 시각 기록
        if last_risk_start_time is None:
            last_risk_start_time = now

        # 지속시간 계산
        risk_duration = now - last_risk_start_time

        # 지속시간이 3초 넘었고, 쿨다운 지났으면 음성 출력
        if risk_duration >= 3 :
            speak_warning()
            last_risk_start_time = now

    elif latest_ear <= 0.26:
        status = "주의"
        last_risk_start_time = None
    
    else:
        last_risk_start_time = None

    return jsonify({
        "ear": latest_ear,
        "status": status,
        "risk_duration" : round(risk_duration, 2)
    })

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=8000,
        use_reloader=False
        )
