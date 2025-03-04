import pygame  # Phát triển trò chơi 2D
import sys  # Thư viện chuẩn của Python để tương tác với hệ điều hành
import os  # Để xử lý đường dẫn tệp
import subprocess  # Để chạy file `game_bat_bong.py` và `game_bat_bong2.py`

# Class của button
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        # Vẽ nút lên màn hình
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

# Tạo màn hình
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')

# Tạo hình ảnh
level1_img = pygame.image.load('level1_btn.png').convert_alpha()
level2_img = pygame.image.load('level2_btn.png').convert_alpha()

# Tạo button
start_button = Button(100, 200, level1_img, 0.8)
exit_button = Button(450, 200, level2_img, 0.8)

# Đường dẫn tới file game_bat_bong.py và game_bat_bong2.py
game1_path = os.path.join(os.getcwd(), 'game_bat_bong.py')
game2_path = os.path.join(os.getcwd(), 'game_bat_bong2.py')

# Vòng lặp game
run = True
while run:
    screen.fill((202, 228, 241))
 # Kiểm tra nút
    if start_button.draw(screen):
        pygame.quit()
        subprocess.run([sys.executable, game1_path])
        sys.exit()
    if exit_button.draw(screen):
        pygame.quit()
        subprocess.run([sys.executable, game2_path])
        sys.exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()
