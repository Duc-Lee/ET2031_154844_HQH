import pygame
import random
import cv2
import mediapipe as mp
import pyautogui
import time

HAND_SIZE_RANDOMIZE = (1.6, 2.4)
HAND_SIZES = (120, 80)
HAND_MOVE_SPEED = {"min": 6, "max": 12}
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

class Hand:
    def __init__(self):
        random_size_value = random.uniform(HAND_SIZE_RANDOMIZE[0], HAND_SIZE_RANDOMIZE[1])
        size = (int(HAND_SIZES[0] * random_size_value), int(HAND_SIZES[1] * random_size_value))
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, size[0], size[1])

        self.images = [pygame.image.load(r"D:\T1 vo dich\Anh_nen_game\tay.png")]
        self.images = [pygame.transform.scale(image, size) for image in self.images]

    def draw(self, surface):
        surface.blit(self.images[0], (self.rect.x, self.rect.y))

    def follow_mediapipe_hand(self, x, y):
        self.rect.center = (x, y)

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (255, 60, 0), self.rect)
# Khởi tạo các mô-đun từ MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(1)
hand = Hand()
last_click_time = 0
click_delay = 0.5
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                h, w, _ = image.shape
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                x = int(hand_landmarks.landmark[9].x * w)
                y = int(hand_landmarks.landmark[9].y * h)

                screen_w, screen_h = pyautogui.size()
                mouse_x = int(x * screen_w / w)
                mouse_y = int(y * screen_h / h)
                pyautogui.moveTo(mouse_x, mouse_y)

                x1 = int(hand_landmarks.landmark[12].x * w)
                y1 = int(hand_landmarks.landmark[12].y * h)
                if y1 > y and time.time() - last_click_time > click_delay:
                    hand_status = "CLOSED"
                    pyautogui.click()
                    last_click_time = time.time()
                else:
                    hand_status = "OPEN"
                cv2.putText(image, hand_status, (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
                hand.follow_mediapipe_hand(x, y)
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
              cap.release()
cv2.destroyAllWindows()
