# main.py
import cv2
import mediapipe as mp
import numpy as np
from ear_utils import calculate_ear
from text_utils import draw_text_korean


# Mediapipe 설정
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)

# 눈 랜드마크 인덱스 (Mediapipe 기준)
LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]

# 눈 좌표 추출 함수
def get_eye_landmarks(landmarks, eye_indices, image_width, image_height):
    return [(int(landmarks[i].x * image_width), int(landmarks[i].y * image_height)) for i in eye_indices]

# EAR 판정 기준
EAR_THRESHOLD = 0.25              # 눈을 감았다고 판단할 EAR 기준값
CLOSED_FRAMES_THRESHOLD = 15      # 연속으로 몇 프레임 이상 감겼을 때 경고
close_counter = 0                 # 눈 감은 프레임 수 카운터

# 웹캠 열기
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            left_eye = get_eye_landmarks(landmarks, LEFT_EYE_IDX, w, h)
            right_eye = get_eye_landmarks(landmarks, RIGHT_EYE_IDX, w, h)

            # EAR 계산
            left_ear = calculate_ear(left_eye)
            right_ear = calculate_ear(right_eye)
            avg_ear = (left_ear + right_ear) / 2.0

            # EAR 출력
            cv2.putText(frame, f"EAR: {avg_ear:.3f}", (30, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)

            # 눈 포인트 시각화
            for (x, y) in left_eye + right_eye:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # 졸음 판별 및 경고 메시지
            if avg_ear < EAR_THRESHOLD:
                close_counter += 1
                if close_counter >= CLOSED_FRAMES_THRESHOLD:
                    frame = draw_text_korean(frame, "졸음 경고!", (30, 150),
                                             font_size=40, color=(0, 0, 255))
            else:
                close_counter = 0

    cv2.imshow("EAR Live", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC 키로 종료
        break

cap.release()
cv2.destroyAllWindows()
