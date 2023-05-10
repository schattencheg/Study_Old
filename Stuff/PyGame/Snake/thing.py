import pygame
import os
from pygame.math import Vector2

class Thing:
    def __init__(self, filename = "Snake\\Assets\Images\\car0.png", 
                    width = 400, height = 400, 
                    speed = 1.0, length = 1, pos_x = 200, pos_y = 200):
        self.width = width
        self.height = height
        self.size = (width, height)
        self.surface = pygame.Surface(self.size)
        self.speed = speed
        self.length = length
        self.pos = (pos_x, pos_y)
        self.filename = filename
        self.directions = [(0,0), (0,1), (1,1), (1,0)]
        self.angle = 0
        
        if self.filename == None or not os.path.exists(self.filename):
            self.image_base = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.polygon(self.image_base, (50, 120, 180), ((0, 0), (0, 50), (50, 50)))
            self.rect_base = self.image_base.get_rect(center=self.pos)
        else:
            self.image_base = pygame.image.load(self.filename).convert_alpha()
            self.rect_base = self.image_base.get_rect(center=self.pos)
        self.image = self.image_base
        self.rect = self.rect_base
        self.position = Vector2(self.pos)
        self.direction = Vector2(0, -1)
        self.pivot = [self.image_base.get_width() / 2, self.image_base.get_height() / 2]
        self.offset = Vector2(self.image_base.get_width() / 2, self.image_base.get_height())
        self.rotated_image = pygame.Surface(self.size)

    def rotater(self, image, angle):
        center = image.get_rect().center
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = center)
        return rotated_image, new_rect

    def rotate(self, surface, angle, pivot, offset):
        """Rotate the surface around the pivot point.

        Args:
            surface (pygame.Surface): The surface that is to be rotated.
            angle (float): Rotate by this angle.
            pivot (tuple, list, pygame.math.Vector2): The pivot point.
            offset (pygame.math.Vector2): This vector is added to the pivot.
        """
        #rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
        rotated_image = pygame.transform.rotate(surface, -angle)  # Rotate the image.
        rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
        # Add the offset vector to the center/pivot point to shift the rect.
        rect = rotated_image.get_rect(center=pivot+rotated_offset)
        return rotated_image, rect  # Return the rotated image and shifted rect.

    def update(self, angle_increment = 0):
        pygame.draw.rect(self.surface, (255,255,255), pygame.Rect(1,1,self.width-1,self.height-1))
        self.position_increment = self.speed
        if self.position_increment != 0.0:
            self.position += self.direction * self.position_increment
            self.rect.center = self.position
        if angle_increment != 0.0:
            self.direction.rotate_ip(angle_increment)
            self.angle += angle_increment
            #self.image = pygame.transform.rotate(self.image, -self.angle)
            #self.rect = self.image.get_rect(center=self.rect.center)
            self.rotated_image, rect = self.rotate(self.image_base, self.angle, self.pivot, self.offset)
        self.surface = self.rotated_image
        #self.surface = self.image

    def update_surface(self):
        pass

    def GetImage(self):
        return self.surface