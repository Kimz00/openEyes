import mediapipe as mp

# Mediapipe 설정
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)

# 눈 랜드마크 인덱스
LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]

def get_eye_landmarks(landmarks, eye_indices, image_width, image_height):
    return [(int(landmarks[i].x * image_width), int(landmarks[i].y * image_height)) for i in eye_indices]

def get_face_mesh():
    return face_mesh

def get_eye_indices():
    return LEFT_EYE_IDX, RIGHT_EYE_IDX
