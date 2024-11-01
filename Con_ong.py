import pygame
import random

CON_ONG_SIZE_RANDOMIZE = (1, 2)
CON_ONG_SIZES = (60, 40)
CON_ONG_MOVE_SPEED = {"min": 3, "max": 6}
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800


class Bee:
    def __init__(self):
        random_size_value = random.uniform(CON_ONG_SIZE_RANDOMIZE[0], CON_ONG_SIZE_RANDOMIZE[1])
        size = (int(CON_ONG_SIZES[0] * random_size_value), int(CON_ONG_SIZES[1] * random_size_value))
        moving_direction, start_pos = self.define_spawn_pos(size)
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0], size[1])

        self.images = [pygame.image.load(r"D:\T1 vo dich\Anh_nen_game\anh_ong.png")]
        self.images = [pygame.transform.scale(image, size) for image in self.images]

        if moving_direction == "right":
            self.images[0] = pygame.transform.flip(self.images[0], True, False)

    def define_spawn_pos(self, size):
        vel = random.uniform(CON_ONG_MOVE_SPEED["min"], CON_ONG_MOVE_SPEED["max"])
        moving_direction = random.choice(("left", "right", "up", "down"))
        if moving_direction == "right":
            start_pos = (-size[0], random.randint(0, SCREEN_HEIGHT - size[1]))
            self.vel = [vel, 0]
        elif moving_direction == "left":
            start_pos = (SCREEN_WIDTH + size[0], random.randint(0, SCREEN_HEIGHT - size[1]))
            self.vel = [-vel, 0]
        elif moving_direction == "up":
            start_pos = (random.randint(0, SCREEN_WIDTH - size[0]), SCREEN_HEIGHT + size[1])
            self.vel = [0, -vel]
        elif moving_direction == "down":
            start_pos = (random.randint(0, SCREEN_WIDTH - size[0]), -size[1])
            self.vel = [0, vel]

        return moving_direction, start_pos

    def move(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        if (self.rect.x < -self.rect.width or
                self.rect.x > SCREEN_WIDTH or
                self.rect.y < -self.rect.height or
                self.rect.y > SCREEN_HEIGHT):
            self.__init__()

    def draw(self, surface):
        surface.blit(self.images[0], (self.rect.x, self.rect.y))
