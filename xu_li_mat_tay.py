import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils # Khởi tạo các đối tượng vẽ và nhận diện tay, khuôn mặt
mp_hands = mp.solutions.hands
mp_face_detection = mp.solutions.face_detection
cap = cv2.VideoCapture(1)
hands = mp_hands.Hands(min_detection_confidence=0.5)
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
while True:
    ret, image = cap.read()
    if not ret:
        break
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    hand_results = hands.process(image)
    face_results = face_detection.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    if face_results.detections:
        for detection in face_results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = image.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Vẽ hình chữ nhật quanh khuôn mặt
    cv2.imshow('Hand and Face Tracker', image)
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break
cap.release()
cv2.destroyAllWindows()
