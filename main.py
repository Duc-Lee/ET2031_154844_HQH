import pygame # Phát triển trò chơi 2D
import sys # Thư viện chuẩn của Python để tương tác với hệ điều hành
import cv2 # Thư viện OpenCV
from cvzone.HandTrackingModule import HandDetector # Xử lí ảnh bằng OpenCV
import random # Thư viện chuẩn -> Xây dựng các giá trị ngẫu nhiên
from pygame import mixer

# Kích thước cửa sổ game
width = 1200
height = 700
cap = cv2.VideoCapture(1)  # Khởi tạo webcam với chỉ số 1
cap.set(3, width)  # Đặt chiều rộng của cửa sổ webcam
cap.set(4, height)  # Đặt chiều cao của cửa sổ webcam

detector = HandDetector(maxHands=1, detectionCon=0.8)  # Khởi tạo đối tượng nhận diện bàn tay
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
InsectImg = []
InsectX = []
InsectY = []
insect_rect = []
insectMoveX = []
insectMoveY = []
numberOfInsects = 10
for i in range(numberOfInsects):
    InsectX.append(random.randint(0, width))
    InsectY.append(random.randint(0, height))
    InsectImg.append(pygame.image.load('ball_32.png').convert_alpha())  # Tạo bóng
    insect_rect.append(InsectImg[i].get_rect(topleft=(InsectX[i], InsectY[i])))  # Vị trí bóng
    insectMoveX.append(10)  # Tốc độ di chuyển bóng theo chiều X
    insectMoveY.append(8)  # Tốc độ di chuyển bóng theo chiều Y

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
    bombMoveX.append(5)  # Tốc độ di chuyển bom theo chiều X
    bombMoveY.append(5)  # Tốc độ di chuyển bom theo chiều Y

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
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))  # Hiển thị điểm
    screen.blit(score, (x, y))

def show_bombs_caught(x, y):
    bombs = font.render("Bombs Caught: " + str(bombs_caught), True, (255, 255, 255))  # Hiển thị bom đã bắt
    screen.blit(bombs, (x, y + 40))

def show_timer():
    if currentTime / 1000 >= 80:
        timer = font.render("Time: " + str(int(101 - currentTime / 1000)), True, (255, 0, 0))  # Thời gian còn lại
    else:
        timer = font.render("Time: " + str(int(101 - currentTime / 1000)), True, (255, 255, 255))
    screen.blit(timer, (1210, 10))
    if currentTime / 1000 >= 100 or game_over:  # Khi kết thúc trò chơi
        gameOver_text = gameOver_font.render("Game Over!", True, (255, 0, 0))  # Hiển thị Game Over
        screen.blit(gameOver_text, (width / 2 - 300, height / 2 - 30))
        if pygame.mouse.get_pressed()[0]:  # Nhấn chuột để chơi lại
            reset_game()  # Gọi hàm để khởi động lại trò chơi

indexes_for_closed_fingers = [8, 12, 16, 20]

def reset_game():
    global score_value, bombs_caught, game_over
    score_value = 0
    bombs_caught = 0
    game_over = False
    for i in range(numberOfInsects):
        insect_rect[i].topleft = (random.randint(0, width), random.randint(0, height))
    for i in range(numberOfBombs):
        bomb_rect[i].topleft = (random.randint(0, width), random.randint(0, height))

##################################################################################################
###################################################################################################
# Game Loop
catch_insect_with_openHand = False
fingers = [0, 0, 0, 0]
while True:
    # Cập nhật thời gian mỗi frame
    currentTime += clock.get_time()

    # Game code
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()

    # opencv code
    success, frame = cap.read()
    hands, frame = detector.findHands(frame)

    # Landmarks value - (x, y, z) * 21
    if hands:
        lmList = hands[0]
        positionOfTheHand = lmList['lmList']
        openHand_rect.left = (positionOfTheHand[9][0] - 200) * 1.5
        openHand_rect.top = (positionOfTheHand[9][1] - 200) * 1.5
        closedHand_rect.left = (positionOfTheHand[9][0] - 200) * 1.5
        closedHand_rect.top = (positionOfTheHand[9][1] - 200) * 1.5

        # open or closed hand
        hand_is_closed = 0  # for playing the sound once when hand is closed
        for index in range(0, 4):
            if positionOfTheHand[indexes_for_closed_fingers[index]][1] > positionOfTheHand[indexes_for_closed_fingers[index] - 2][1]:
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
                for iteration in range(numberOfInsects):
                    if openHand_rect.colliderect(insect_rect[iteration]) and catch_insect_with_openHand:
                        score_value += 1
                        catching_sound.play()
                        catch_insect_with_openHand = False
                        insect_rect[iteration] = InsectImg[iteration].get_rect(topleft=(random.randint(0, width), random.randint(0, height)))

                catch_insect_with_openHand = False
            else:
                screen.blit(openHandImg, openHand_rect)
                hand_is_closed = 1
                for iterate in range(numberOfInsects):
                    if openHand_rect.colliderect(insect_rect[iterate]):
                        catch_insect_with_openHand = True

    # Opencv Screen
    # Resize webcam frame to a smaller size (you can adjust the scale factor here)
    frame_resized = cv2.resize(frame, (400, 400))  # Resize webcam
    cv2.imshow("webcam", frame_resized)

    # Game screen
    # placing and moving Insects
    for i in range(numberOfInsects):
        # moving X
        insect_rect[i].right += insectMoveX[i]
        if insect_rect[i].right <= 16:
            insectMoveX[i] += 10
        elif insect_rect[i].right >= width:
            insectMoveX[i] -= 10

        # moving Y
        insect_rect[i].top += insectMoveY[i]
        if insect_rect[i].top <= 0:
            insectMoveY[i] += 8
        elif insect_rect[i].top >= height - 32:
            insectMoveY[i] -= 8
        screen.blit(InsectImg[i], insect_rect[i])

    # placing and moving Bombs
    for i in range(numberOfBombs):
        bomb_rect[i].top += bombMoveY[i]
        if bomb_rect[i].top <= 0:
            bombMoveY[i] += 5
        elif bomb_rect[i].top >= height - 32:
            bombMoveY[i] -= 5
        screen.blit(BombImg[i], bomb_rect[i])

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
