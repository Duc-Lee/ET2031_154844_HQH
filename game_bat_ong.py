import pygame
import cv2
import sys
import random
from Con_ong import Bee
from bom import Bomb
from tay import Hand

pygame.init()

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800
pygame.display.set_caption("Game Bắt Ong")
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

background_path = r"D:\T1 vo dich\Anh_nen_game\anh_nen.jpg"

# Khởi tạo các đối tượng
bees = [Bee() for _ in range(15)]
bombs = [Bomb() for _ in range(6)]
tay1 = Hand()
try:
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Không tìm thấy tệp ảnh nền! Vui lòng kiểm tra đường dẫn. Lỗi: {e}")
    pygame.quit()
    sys.exit()

cap = cv2.VideoCapture(1)
# Biến điểm số và đếm bom
score = 0
bomb_count = 0
font = pygame.font.Font(None, 40)
# Hàm di chuyển ong và bom
def move_objects():
    for bee in bees:
        bee.rect.x += random.choice([-1, 1]) * 1
        bee.rect.y += random.choice([-1, 1]) * 1
        bee.rect.x = max(0, min(SCREEN_WIDTH - bee.rect.width, bee.rect.x))
        bee.rect.y = max(0, min(SCREEN_HEIGHT - bee.rect.height, bee.rect.y))
    for bomb in bombs:
        bomb.rect.x += random.choice([-1, 1]) * 1
        bomb.rect.y += random.choice([-1, 1]) * 1
        bomb.rect.x = max(0, min(SCREEN_WIDTH - bomb.rect.width, bomb.rect.x))
        bomb.rect.y = max(0, min(SCREEN_HEIGHT - bomb.rect.height, bomb.rect.y))
# Hàm kiểm tra va chạm
def check_collisions():
    global score, bomb_count
    hand_rect = tay1.rect
    for bee in bees[:]:
        if hand_rect.colliderect(bee.rect):
            score += 1
            bees.remove(bee)
            break
    for bomb in bombs[:]:
        if hand_rect.colliderect(bomb.rect):
            bomb_count += 1
            bombs.remove(bomb)
            break
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:  #ktr nhan chuot
            check_collisions()
    # Lấy vị trí chuột
    mouse_x, mouse_y = pygame.mouse.get_pos()
    tay1.follow_mediapipe_hand(mouse_x, mouse_y)
    # Di chuyển các con ong và bom
    move_objects()
    # Hiển thị trò chơi Pygame
    SCREEN.blit(background, (0, 0))
    for bee in bees:
        SCREEN.blit(bee.images[0], bee.rect.topleft)
    for bomb in bombs:
        SCREEN.blit(bomb.images[0], bomb.rect.topleft)
    hand_x, hand_y = tay1.rect.topleft  # Lấy vị trí tay
    SCREEN.blit(tay1.images[0], (hand_x, hand_y))  # Vẽ hình ảnh tay
    # Hiển thị điểm số
    score_text = font.render(f"Diem: {score}", True, (255, 255, 255))  # Màu trắng
    SCREEN.blit(score_text, (SCREEN_WIDTH - 150, 10))  # Vị trí ở góc phải

    # Kiểm tra thua game
    if bomb_count >= 3:
        game_over_text = font.render("GAME OVER! NHAN Q DE CHOI LAI.", True, (255, 0, 0))
        SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        pygame.display.flip()  # Cập nhật màn hình
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    cap.release()
                    cv2.destroyAllWindows()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    waiting = False
                    score = 0
                    bomb_count = 0
                    bees = [Bee() for _ in range(10)]
                    bombs = [Bomb() for _ in range(4)]
    pygame.display.flip()

cap.release()
pygame.quit()
sys.exit()

