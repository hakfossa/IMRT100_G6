## no longer drive logic

#testbed

import pygame

mp3_path = 'space_core_quotes.wav'

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(mp3_path)
pygame.mixer.music.play()

clock = pygame.time.Clock()

while True: # main loop
    clock.tick(60)