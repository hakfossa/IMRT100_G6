import pygame
import random
from math import cos, sin, pi
import os, sys
from pygame.locals import *

#endrer working directiory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#starter pygame
pygame.init()

#fps limiter
FPS = 30
FPS_CONTROLLER = pygame.time.Clock()

#farger
BLACK = (0,0,0)

#setup av display
screenX = 800
screenY = 480
DISPLAY = pygame.display.set_mode((screenX, screenY))
DISPLAY.fill(BLACK)
pygame.display.set_caption("space_core")
_fullscreen = False

class Core_eye(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("eye_space_core.png")
        self.rect = self.image.get_rect()
        self.x = screenX/2
        self.y = screenY/2
        self.rect.center = (self.x, self.y)

        # movement of eye
        self.stationary = True
        self.angle = 0
        self._SPEED = 40
        self.speed_x = 30
        self.speed_y = 15
        self.ticks_left = 0
        
    

    def update(self):

        self.check_move()

        if self.stationary:
            self.jitter()
        else:
            self.move()

        self.ticks_left -= 1



        # only updates if changes are inside boundries
        if self.within_boundries():
            self.rect.center = (self.x, self.y)
        else:
            self.x, self.y = self.rect.centerx, self.rect.centery
            self.stationary = True
    

    def draw(self, surface):
        surface.blit(self.image, self.rect)


    def within_boundries(self):
        if (self.x > screenX-135 or
        self.x < 135 or 
        self.y > screenY-135 or
        self.y < 135):
            return False
        else:
            return True

    
    def jitter(self):
        x_random = random.randint(-2, 2)
        y_random = random.randint(-2, 2)
        self.x += x_random
        self.y += y_random
        

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
    

    def random_movement(self):
        angle = random.randint(0, 36)
        rad = 2*pi * angle/36
        self.speed_x = cos(rad)*self._SPEED*2
        self.speed_y = sin(rad)*self._SPEED
        print("angle:", angle)


    def check_move(self):
        if self.ticks_left == 0:
            if self.stationary:
                self.random_movement()
                self.ticks_left = 30
                self.stationary = False
            
            else:
                self.stationary = True
                self.ticks_left = random.randint(30, 90)




## --- eyelid class --- ##


class Eyelid(pygame.sprite.Sprite):
    
    def __init__(self, upper=True):
        super().__init__()
        self.upper = upper

        self.image = pygame.image.load('eyelid.png')
        self.rect = self.image.get_rect()
        self.rect.center = (screenX/2, -screenY/2+50)
        self.stationary = True
        self.move_commands = []


    def update(self):
        """ if self.stationary:
            self.jitter() """
        




    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def jitter(self):
        y_random = random.randint(-1, 1)
        self.rect.centery += y_random



eye = Core_eye()
upper = Eyelid()



while True:


    pygame.display.update()
       
    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()

            elif event.key == K_f:
                if _fullscreen:
                    DISPLAY = pygame.display.set_mode((screenX, screenY))
                    _fullscreen = False
                else:
                    DISPLAY = pygame.display.set_mode((screenX, screenY), pygame.FULLSCREEN)
                    _fullscreen = True
    
    eye.update()
    upper.update()
    

    DISPLAY.fill(BLACK)
    eye.draw(DISPLAY)
    upper.draw(DISPLAY)

    FPS_CONTROLLER.tick(FPS)
