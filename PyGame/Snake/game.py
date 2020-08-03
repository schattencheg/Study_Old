import pygame
import math
from thing import Thing 

class Game:
    def __init__(self, filename, count):
        pygame.init()
        width = 500
        height = 500
        gameDisplay = pygame.display.set_mode((width,height))
        pygame.display.set_caption('Caption')
        clock = pygame.time.Clock()
        loop = True
        self.instances = []
        self.rects = []
        sector_count = math.ceil(math.sqrt(count))
        angle_increment_base = 1
        angle_increment = 0.0

        for i in range(count):
            instance = Thing(filename, width = width, height = height, speed = 1,
                                length = 1, pos_x = width / 2, pos_y = height / 2)
            self.instances.append(instance)
            x = i % sector_count
            y = i // sector_count
            self.sector_width = round(min(width,height) / sector_count)
            self.rects.append((x * self.sector_width, y * self.sector_width, (x + 1) * self.sector_width, (y + 1) * self.sector_width))

        while loop:
            gameDisplay.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        loop = False
                    if event.key == pygame.K_RIGHT:
                        angle_increment = angle_increment_base
                    if event.key == pygame.K_LEFT:
                        angle_increment = -angle_increment_base
                    #if event.key == pygame.K_UP:
                    #    position_increment = position_increment_base
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        angle_increment = 0.0
                    if event.key == pygame.K_LEFT:
                        angle_increment = 0.0
                    #if event.key == pygame.K_UP:
                    #    position_increment = 0.0

            for i in range(count):
                instance = self.instances[i]
                instance.update(angle_increment)
                image = instance.GetImage()
                gameDisplay.blit(pygame.transform.scale(image,(self.sector_width, self.sector_width)), self.rects[i])

            pygame.display.update()
            clock.tick(100)

game = Game(count = 1, filename = "Assets\Images\\car0.png")