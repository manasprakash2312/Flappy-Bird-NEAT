import pygame
import neat
import time
import os
import random

WINDOW_HEIGHT = 500
WINDOW_WIDTH = 800

bird_pos = [pygame.transform.scale2x(pygame.image.load(os.path.join('sprites', 'bird1.png'))),
            pygame.transform.scale2x(pygame.image.load(os.path.join('sprites', 'bird2.png'))),
            pygame.transform.scale2x(pygame.image.load(os.path.join('sprites', 'bird3.png')))]
pipe = pygame.transform.scale2x(pygame.image.load(os.path.join('sprites', 'pipe.png')))
base = pygame.transform.scale2x(pygame.image.load(os.path.join('sprites', 'base.png')))
bg = pygame.transform.scale2x(pygame.image.load(os.path.join('sprites', 'bg.png')))


class Bird:
    sprites = bird_pos
    rotation_angle = 25  # Bird will tilt at 20deg
    rotation_velocity = 5
    animation_time = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = y
        self.img_count = 0
        self.sprite = self.sprites[0]

    def jump(self):
        self.velocity = -10.5
        self.height = self.y

    def move(self):
        self.tick_count += 1
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2

        if displacement >= 16:
            displacement = 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.rotation_angle:
                self.tilt = self.rotation_angle

            else:
                if self.tilt > -90:
                    self.tilt -= self.rotation_velocity

    def draw(self, window):
        self.img_count += 1

        if self.img_count < self.animation_time:
            self.sprite = self.sprites[0]

        elif self.img_count < self.animation_time * 2:
            self.sprite = self.sprites[1]

        elif self.img_count < self.animation_time * 3:
            self.sprite = self.sprites[2]

        elif self.img_count < self.animation_time * 4:
            self.sprite = self.sprites[1]

        elif self.img_count == self.animation_time * 4 + 1:
            self.sprite = self.sprites[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.sprite = self.sprites[1]
            self.img_count = self.animation_time * 2

        rotated_sprite = pygame.transform.rotate(self.sprite, self.tilt)
        new_rect = rotated_sprite.get_rect(center=self.sprite.get_rect(topleft=(self.x, self.y)).center)

        window.blit(rotated_sprite, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.sprite)

class Pipe:
    gap = 200
    velocity = 5

    def __init__(self):
        pass

def draw_window(window, bird):
    window.blit(bg, (0, 0))
    bird.draw(window)
    pygame.display.update()

def main():
    bird = Bird(200, 200)

    window = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    clock = pygame.time.Clock()

    run = True

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bird.move()
        draw_window(window, bird)

    pygame.quit()
    quit()

main()