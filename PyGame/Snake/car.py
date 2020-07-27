import pygame
import os

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()
loop = True

filename = "Snake\\Assets\Images\\car0.png"
if filename == None or not os.path.exists(filename):
    image_base = pygame.Surface((70, 50), pygame.SRCALPHA)
    pygame.draw.polygon(image_base, (50, 120, 180), ((0, 0), (0, 50), (70, 25)))
    car_rect = image_base.get_rect()
else:
    image_base = pygame.image.load(filename).convert_alpha()
    car_rect = image_base.get_rect()
    #car_rect.centerx = car_rect.width / 2
    #car_rect.centery = car_rect.height / 2

def rot_center(image, angle):
    center = image.get_rect().center
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = center)
    return rotated_image, new_rect

x = 50
y = 50
angle = 0
image = image_base
angle_increment = 0.0
increment_base = 1.0

while loop:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                loop = False
            if event.key == pygame.K_RIGHT:
                angle_increment = -increment_base
            if event.key == pygame.K_LEFT:
                angle_increment = increment_base
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                angle_increment = 0.0
            if event.key == pygame.K_LEFT:
                angle_increment = 0.0
        print(event)
    if angle_increment != 0.0:
        angle += angle_increment
        image, car_rect = rot_center(image_base, angle)

    gameDisplay.fill((255,255,255))
    gameDisplay.blit(image, car_rect)
    pygame.display.update()
    clock.tick(100)
