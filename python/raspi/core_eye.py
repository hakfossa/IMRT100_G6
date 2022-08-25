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
        x_random = random.randint(-1, 1)
        y_random = random.randint(-1, 1)
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
        #print("angle:", angle)


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
        if upper:
            self.direction_modifier = 1
        else:
            self.direction_modifier = -1

        self.image = pygame.image.load('eyelid.png')
        self.rect = self.image.get_rect()
        self.rect.center = (screenX/2, screenY/2 - int(self.direction_modifier)*screenY)
        self.speed = 0
        self.opening = False
        self.blinking = False
        self.squinting = False
        self.squint_timer = 0



    def update(self):
        if self.blinking or self.squinting:
            if (self.blinking and
            0 < self.rect.centery < screenY and 
            not self.opening):
                self.open_eye()
                

            elif (self.squinting and
            -screenY/3 < self.rect.centery < screenY*1.3 and
            not self.opening):
                if self.squint_timer > 0:
                    self.squint_timer -= 1
                else:
                    self.open_eye()
                    


            elif (self.opening and (self.rect.centery < -screenY/2 or
            self.rect.centery > screenY*1.5)):
                self.speed = 0
                self.blinking = False
                self.squinting = False


            else:
                self.rect.centery += self.speed*50

            


    def draw(self, surface):
        surface.blit(self.image, self.rect)


    def close_eye(self):
        self.opening = False
        self.speed = self.direction_modifier


    def open_eye(self):
        self.opening = True
        self.speed = self.direction_modifier*-1


    def blink(self):
        self.blinking = True
        self.close_eye()


    def squint(self, squint_time):
        self.squinting = True
        self.squint_timer = squint_time
        self.close_eye()

    
        
class Eyelids():
    
    def __init__(self):
        self.upper = Eyelid()
        self.lower = Eyelid(False)

    def update(self):
        self.upper.update()
        self.lower.update()

    def draw(self, surface):
        self.upper.draw(surface)
        self.lower.draw(surface)

    def blink(self):
        self.upper.blink()
        self.lower.blink()
    
    def squint(self):
        squint_time = random.randint(30, 80)
        self.upper.squint(squint_time)
        self.lower.squint(squint_time)


class Eyelid_controller():
    
    def __init__(self, eyelids):
        self.eyelids = eyelids
        self.timer = 0

    def random_event(self):
        event = random.choice(["blink", "squint", "blink"])
        if event == "blink":
            self.eyelids.blink()
        elif event == "squint":
            self.eyelids.squint()
        print(event)
        self.add_time()

    def add_time(self):
        self.timer = random.randint(20, 100)
    
    def update(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.random_event()




eye = Core_eye()
eyelids = Eyelids()
eyelid_controller = Eyelid_controller(eyelids)


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
            
            elif event.key == K_b:
                eyelids.blink()
            
            
            elif event.key == K_s:
                print("s")
                eyelids.squint()
    
    eye.update()
    eyelids.update()
    eyelid_controller.update()

    DISPLAY.fill(BLACK)
    eye.draw(DISPLAY)
    eyelids.draw(DISPLAY)

    FPS_CONTROLLER.tick(FPS)
