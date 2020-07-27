import pygame
from pygame.math import Vector2
import os

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()
loop = True
pos=(120, 120)

filename = "Snake\\Assets\Images\\car0.png"
if filename == None or not os.path.exists(filename):
    image_base = pygame.Surface((70, 50), pygame.SRCALPHA)
    pygame.draw.polygon(image_base, (50, 120, 180), ((0, 0), (0, 50), (70, 25)))
    car_rect = image_base.get_rect(center=pos)
else:
    image_base = pygame.image.load(filename).convert_alpha()
    car_rect = image_base.get_rect(center=pos)
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
angle_increment_base = 1.0
position_increment = 0.0
position_increment_base = 1.0

position = Vector2(pos)
direction = Vector2(0, -1) 

while loop:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                loop = False
            if event.key == pygame.K_RIGHT:
                angle_increment = angle_increment_base
            if event.key == pygame.K_LEFT:
                angle_increment = -angle_increment_base
            if event.key == pygame.K_UP:
                position_increment = position_increment_base
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                angle_increment = 0.0
            if event.key == pygame.K_LEFT:
                angle_increment = 0.0
            if event.key == pygame.K_UP:
                position_increment = 0.0
        #print(event)
    if position_increment != 0.0:
        position += direction * position_increment
        car_rect.center = position
    if angle_increment != 0.0:
        direction.rotate_ip(angle_increment)
        angle += angle_increment
        image = pygame.transform.rotate(image_base, -angle)
        car_rect = image.get_rect(center=car_rect.center)
        #image, car_rect = rot_center(image_base, angle)

    gameDisplay.fill((255,255,255))
    
    rect_image = pygame.Surface((car_rect.width, car_rect.height), pygame.SRCALPHA)
    pygame.draw.polygon(rect_image, (50, 120, 180), ((0, 0), (car_rect.width, 0), (car_rect.width, car_rect.height), (0, car_rect.height)))
    gameDisplay.blit(rect_image, car_rect)

    gameDisplay.blit(image, car_rect)
    pygame.display.update()
    clock.tick(100)
