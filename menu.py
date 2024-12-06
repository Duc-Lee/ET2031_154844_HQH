import pygame
import sys
import os
import subprocess
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
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        # Draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
# Tạo màn hình
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')

# Tạo hình ảnh
start_img = pygame.image.load('start_btn.png').convert_alpha()
exit_img = pygame.image.load('exit_btn.png').convert_alpha()

# Tạo button
start_button = Button(100, 200, start_img, 0.8)
exit_button = Button(450, 200, exit_img, 0.8)

# Đường dẫn tới file game_bat_bong.py
game_path = os.path.join(os.getcwd(), 'game_bat_bong.py')
# Vòng lặp game
run = True
while run:
    screen.fill((202, 228, 241))
    # Kiểm tra nút
    if start_button.draw(screen):
        pygame.quit()
        subprocess.run([sys.executable, game_path])
        sys.exit()
    if exit_button.draw(screen):
        run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()
