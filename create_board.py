import pygame
import sys
import numpy as np

pygame.init()




#global variables
row_size=6
column_size=7
board=np.zeros((row_size,column_size))
np.flip(board,0)
game="True"
turn=0
row_count=[0,0,0,0,0,0,0]
win=0
size=100
height=int((row_size+1)*size)
width=int(column_size*size)
blue=(0,0,255)
black=(0,0,0)
red=(255,0,0)
yellow=(255,255,0)


#creating the screen of the game
def create():
    screen_size = (width, height)
    screen = pygame.display.set_mode(screen_size)
    pygame.draw.rect(screen, blue, (0, size, width, (row_size * size)))
    for i in range(row_size):
        for j in range(column_size):
            pygame.draw.circle(screen, black, (int((j * size) + size / 2), int(size + size / 2 + (i * size))),
                               int(size / 2 - 5))
    pygame.display.update()



