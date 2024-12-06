import pygame # Phát triển trò chơi 2D
import sys # Thư viện chuẩn của Python để tương tác với hệ điều hành
import cv2 # Thư viện OpenCV
import os  # Để xử lý đường dẫn tệp
import subprocess  # Để chạy file `menu.py`
from cvzone.HandTrackingModule import HandDetector # Xử lí ảnh bằng OpenCV
import random # Thư viện chuẩn -> Xây dựng các giá trị ngẫu nhiên
from pygame import mixer

# Kích thước cửa sổ game
width = 1200
height = 700
cap = cv2.VideoCapture(1)  # Khởi tạo webcam với chỉ số 1
cap.set(3, width)  # Đặt chiều rộng của cửa sổ webcam
cap.set(4, height)  # Đặt chiều cao của cửa sổ webcam
detector = HandDetector(maxHands=1, detectionCon=0.9)  # Khởi tạo đối tượng nhận diện bàn tay
pygame.init()  # Khởi tạo Pygame

mixer.music.load('background.mp3')  # Tải nhạc nền
mixer.music.play(loops=-1)  # Phát nhạc nền lặp lại vô hạn
closedHand_sound = mixer.Sound('slap.mp3')  # Âm thanh khi tay đóng lại
catching_sound = mixer.Sound('catching_sound.wav')  # Âm thanh khi bắt được bóng

# xác định màn hình
screen = pygame.display.set_mode((width, height))  # Tạo cửa sổ game với kích thước đã định
clock = pygame.time.Clock()  # Đặt đối tượng clock để điều khiển tốc độ FPS
currentTime = 1  # Thời gian hiện tại của trò chơi (dùng để đếm ngược)

# Khởi tạo quả bóng
pygame.display.set_caption("Catch Ball")
icon = pygame.image.load('ball_32.png').convert_alpha()
pygame.display.set_icon(icon)
backgroundImg = pygame.image.load('TennisBack.png').convert()
# Tải hình ảnh nút Back
back_img = pygame.image.load('button_back.png').convert_alpha()  # Đường dẫn tới ảnh nút Back
back_img = pygame.transform.scale(back_img, (250, 80))  # kích thước
back_button_rect = back_img.get_rect(center=(width / 2, height - 100))  # vị trí

# Khởi tạo các đối tượng của trò chơi
playerPosition = [370, 480]
playerMovement = [0, 0]
x = width / 2 - 64
y = height / 2 - 64
openHandImg = pygame.image.load('openHand.png').convert_alpha()  # Hình ảnh tay mở
openHandImg = pygame.transform.scale(openHandImg, (128, 128))  # Thay đổi kích thước tay mở
openHand_rect = openHandImg.get_rect(topleft=(x, y))  # Vị trí tay mở

closedHandImg = pygame.image.load('closedHand.png').convert_alpha()  # Hình ảnh tay đóng
closedHandImg = pygame.transform.scale(closedHandImg, (128, 128))  # Thay đổi kích thước tay đóng
closedHand_rect = closedHandImg.get_rect(topleft=(x, y))  # Vị trí tay đóng

# Tạo bóng // Tạo danh sách liên kết lưu thông tin về quả bóng
BallImg = []
BallX = []
BallY = []
Ball_rect = []
BallMoveX = []
BallMoveY = []
numberOfBalls = 10
for i in range(numberOfBalls):
    BallX.append(random.randint(0, width))
    BallY.append(random.randint(0, height))
    BallImg.append(pygame.image.load('ball_32.png').convert_alpha())  # Tạo bóng
    Ball_rect.append(BallImg[i].get_rect(topleft=(BallX[i], BallY[i])))  # Vị trí bóng
    BallMoveX.append(6)  # Tốc độ di chuyển bóng theo chiều X
    BallMoveY.append(4)  # Tốc độ di chuyển bóng theo chiều Y

# Bombs // Tạo danh sách liên kết lưu thông tin về quả bóng
BombImg = []
BombX = []
BombY = []
bomb_rect = []
bombMoveX = []
bombMoveY = []
numberOfBombs = 5
for i in range(numberOfBombs):
    BombX.append(random.randint(0, width))
    BombY.append(random.randint(0, height))
    BombImg.append(pygame.image.load('bomb.png').convert_alpha())  # Tạo bom
    BombImg[i] = pygame.transform.scale(BombImg[i], (40, 40))  # Thay đổi kích thước bom
    bomb_rect.append(BombImg[i].get_rect(topleft=(BombX[i], BombY[i])))  # Vị trí bom
    bombMoveX.append(6)  # Tốc độ di chuyển bom theo chiều X
    bombMoveY.append(4)  # Tốc độ di chuyển bom theo chiều Y

# Game Texts
score_value = 0
bombs_caught = 0  # Biến đếm số bom bắt được
game_over = False
font = pygame.font.Font('freesansbold.ttf', 32) #Dùng hàm font tạo ra văn bản đếm số
gameOver_font = pygame.font.Font('freesansbold.ttf', 100)
textX = 10
textY = 10
# Hiện điểm và bom bắt được
def show_score(x, y):
    score = font.render("Point : " + str(score_value), True, (0, 0, 0))  # Hiển thị điểm
    screen.blit(score, (x, y))

def show_bombs_caught(x, y):
    bombs = font.render("Bom : " + str(bombs_caught), True, (0, 0, 0))  # Hiển thị bom đã bắt
    screen.blit(bombs, (x, y + 40))

def show_timer():
    remaining_time = int(61 - currentTime / 1000)
    timer_color = (255, 0, 0) if remaining_time <= 20 else (0, 0, 0)  # Đổi màu khi còn thời gian <= 20s
    timer = font.render(f"Time: {remaining_time}", True, timer_color)
    screen.blit(timer, (1000, 10))
    if remaining_time <= 0 or game_over:
        show_game_over()
# Khai báo font cho thông báo "Click chuột để chơi lại!"
click_font = pygame.font.Font(None, 50)
# Game Over Screen Function
def show_game_over():
    global game_over
    gameOver_text = gameOver_font.render("Game Over!", True, (255, 0, 0))
    gameOver_rect = gameOver_text.get_rect(center=(width / 2, height / 2 - 30))
    screen.blit(gameOver_text, gameOver_rect)

    # Hiển thị thông báo "Click chuột để chơi lại!"
    cclick_text = click_font.render("Click mouse for reset!", True, (0, 0, 0))
    cclick_rect = cclick_text.get_rect(center=(width / 2, height / 2 + 50))
    screen.blit(cclick_text, cclick_rect)
    # Hiển thị nút "Back"
    screen.blit(back_img, back_button_rect)
    # Kiểm tra sự kiện nhấn chuột
    mouse_pos = pygame.mouse.get_pos()  # Lấy tọa độ chuột
    if pygame.mouse.get_pressed()[0]:  # Nếu nhấn chuột trái
        if back_button_rect.collidepoint(mouse_pos):  # Nếu nhấn vào nút "Back"
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            subprocess.run([sys.executable, os.path.join(os.getcwd(), 'menu.py')])
            sys.exit()
        if cclick_rect.collidepoint(mouse_pos):  # Nếu nhấn vào thông báo chơi lại
            reset_game()
indexes_for_closed_fingers = [8, 12, 16, 20]

def reset_game():
    global score_value, bombs_caught, game_over, currentTime
    score_value = 0
    bombs_caught = 0
    game_over = False
    currentTime = 1
    for i in range(numberOfBalls):
        Ball_rect[i].topleft = (random.randint(0, width), random.randint(0, height))
    for i in range(numberOfBombs):
        bomb_rect[i].topleft = (random.randint(0, width), random.randint(0, height))

##################################################################################################
###################################################################################################
# Game Loop
# Game Loop
catch_insect_with_openHand = False
fingers = [0, 0, 0, 0]
while True:
    # Game code
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()

    if not game_over:  # Chỉ tiếp tục các hoạt động này nếu trò chơi chưa kết thúc
        # Cập nhật thời gian mỗi frame
        currentTime += clock.get_time()
        # opencv code
        success, frame = cap.read()
        hands, frame = detector.findHands(frame)

        # Landmarks value - (x, y, z) * 21
        if hands:
            lmList = hands[0]
            positionOfTheHand = lmList['lmList']
            openHand_rect.left = width - ((positionOfTheHand[9][0] - 200) * 1.5)
            openHand_rect.top = (positionOfTheHand[9][1] - 200) * 1.5
            closedHand_rect.left = width - ((positionOfTheHand[9][0] - 200) * 1.5)
            closedHand_rect.top = (positionOfTheHand[9][1] - 200) * 1.5
            # open or closed hand
            hand_is_closed = 0  # for playing the sound once when hand is closed
            for index in range(0, 4):
                if positionOfTheHand[indexes_for_closed_fingers[index]][1] > \
                        positionOfTheHand[indexes_for_closed_fingers[index] - 2][1]:
                    fingers[index] = 1
                else:
                    fingers[index] = 0
                if fingers[0] * fingers[1] * fingers[2] * fingers[3]:
                    # playing close hand sound
                    if hand_is_closed and catch_insect_with_openHand == False:
                        closedHand_sound.play()
                    hand_is_closed = 0
                    screen.blit(closedHandImg, closedHand_rect)
                    # detect catching
                    for iteration in range(numberOfBalls):
                        if openHand_rect.colliderect(Ball_rect[iteration]) and catch_insect_with_openHand:
                            score_value += 1
                            catching_sound.play()
                            catch_insect_with_openHand = False
                            Ball_rect[iteration] = BallImg[iteration].get_rect(
                                topleft=(random.randint(0, width), random.randint(0, height)))

                    catch_insect_with_openHand = False
                else:
                    screen.blit(openHandImg, openHand_rect)
                    hand_is_closed = 1
                    for iterate in range(numberOfBalls):
                        if openHand_rect.colliderect(Ball_rect[iterate]):
                            catch_insect_with_openHand = True
        # Opencv Screen
        frame_resized = cv2.resize(frame, (400, 400))  # Resize webcam
        cv2.imshow("webcam", frame_resized)

    # Game screen
    # placing and moving Balls
    for i in range(numberOfBalls):
        if not game_over:  # Chỉ di chuyển các bóng khi game chưa kết thúc
            # moving X
            Ball_rect[i].right += BallMoveX[i]
            if Ball_rect[i].right <= 16:
                BallMoveX[i] += 10
            elif Ball_rect[i].right >= width:
                BallMoveX[i] -= 10

            # moving Y
            Ball_rect[i].top += BallMoveY[i]
            if Ball_rect[i].top <= 0:
                BallMoveY[i] += 8
            elif Ball_rect[i].top >= height - 32:
                BallMoveY[i] -= 8
            screen.blit(BallImg[i], Ball_rect[i])

    # Di chuyển quả bom
    for i in range(numberOfBombs):
        if not game_over:
            # Moving X
            bomb_rect[i].right += bombMoveX[i]
            if bomb_rect[i].right <= 16 or bomb_rect[i].right >= width:
                bombMoveX[i] *= -1  # Đảo chiều chuyển động khi chạm vào mép trái/phải
            # Moving Y
            bomb_rect[i].top += bombMoveY[i]
            if bomb_rect[i].top <= 0 or bomb_rect[i].top >= height - 32:
                bombMoveY[i] *= -1  # Đảo chiều khi chạm vào mép trên/dưới
            screen.blit(BombImg[i], bomb_rect[i])
    if currentTime >= 60000:  # 60 giây = 60000 milliseconds
        game_over = True
    # Logic for catching Bombs
    for i in range(numberOfBombs):
        if openHand_rect.colliderect(bomb_rect[i]):
            bombs_caught += 1
            bomb_rect[i] = BombImg[i].get_rect(topleft=(random.randint(0, width), random.randint(0, height)))
            if bombs_caught == 3:
                game_over = True
    # Display score and timer
    show_score(textX, textY)
    show_bombs_caught(textX, textY)
    show_timer()
    pygame.display.update()
    clock.tick(60)  # 60 FPS
