from flask import Flask, render_template, jsonify
import threading
import time
import cv2
import mediapipe as mp
from ear_utils import calculate_ear
from face_eye_detection import get_eye_landmarks
import pyttsx3

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

# 음성 엔진 초기화
engine = pyttsx3.init()

def speak_warning():
    engine.say("경고! 졸음 상태가 감지되었습니다.")
    engine.runAndWait()

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
    global last_voice_time
    now = time.time()
    status = "정상"

    if latest_ear < 0.23:
        status = "위험"
        if now - last_voice_time > cooldown_seconds:
            threading.Thread(target=speak_warning).start()
            last_voice_time = now
    elif latest_ear < 0.26:
        status = "주의"

    return jsonify({
        "ear": latest_ear,
        "status": status
    })

if __name__ == "__main__":
    app.run(debug=True)
