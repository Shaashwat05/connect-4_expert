import socket
import os
import subprocess
import pygame
import sys
import numpy as np
import time
import math
import pickle

pygame.init()



#global variables
row_size=6
column_size=7
board=np.zeros((row_size,column_size))
np.flip(board,0)
turn=0
row_count=[0,0,0,0,0,0,0]
size=100
height=int((row_size+1)*size)
width=int(column_size*size)
blue=(0,0,255)
black=(0,0,0)
red=(255,0,0)
yellow=(255,255,0)
myfont = pygame.font.SysFont("monospace", 75)



s=socket.socket()
host="192.168.43.32"
port=9999

s.connect((host,port))


#creating the screen of the game
screen_size=(width,height)
screen=pygame.display.set_mode(screen_size)
pygame.draw.rect(screen,blue,(0,size,width,(row_size*size)))
for i in range(row_size):
    for j in  range(column_size):
        pygame.draw.circle(screen,black,(int((j*size)+size/2),int(size+size/2+(i*size))),int(size/2-5))
pygame.display.set_caption("1 player")
pygame.display.update()



def validity(col):
    return board[row_size-1][col]==0

def get_next_open_window(col):
    for r in range(row_size):
        if board[r][col] == 0:
            return r

#putting the repective player's pieces in their positions
def put_turn(board,row,col,plr):
    board[row,col]=plr
    if(plr==1):
        pygame.draw.circle(screen,red,(int((col)*size+size/2),int((5-row_count[col])*size+size+size/2)),int(size/2-5))
    else:
        pygame.draw.circle(screen,yellow, (int((col)*size+size/2),int((5-row_count[col])*size+size+size/2)),int(size/2-5))
    pygame.display.update()
    row_count[col]+=1


#checking win condition
def win_cond(plr):

    #horizontal check
    for i in range(row_size):
        for j in range(column_size-3):
            if(board[i][j]==plr and board[i][j+1]==plr and board[i][j+2]==plr and board[i][j+3]==plr):
                return 1

    #vertical check
    for i in range(row_size-3):
        for j in range(column_size):
            if(board[i][j]==plr and board[i+1][j]==plr and board[i+2][j]==plr and board[i+3][j]==plr):
                return 1


    #positive diagonal(slope) check
    for i in range(row_size-3):
        for j in range(column_size-3):
            if(board[i][j]==plr and board[i+1][j+1]==plr and board[i+2][j+2]==plr and board[i+3][j+3]==plr):
                return 1


    #negative diagonal(slope) check
    for i in range(row_size-3):
        for j in range(3,column_size):
            if(board[i][j]==plr and board[i+1][j-1]==plr and board[i+2][j-2]==plr and board[i+3][j-3]==plr):
                return 1

    return 0



def human_turn(plr,win):
    game=True
    while game:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                # sys.exit()
            if (event.type == pygame.MOUSEMOTION):
                poss = event.pos[0]
                pygame.draw.rect(screen, black, (0, 0, width, size))
                if (plr == 1):
                    pygame.draw.circle(screen, red, (poss, int(size / 2)), int(size / 2 - 5))
                pygame.display.update()

            if (event.type == pygame.MOUSEBUTTONDOWN):
                # print("player ", ((turn % 2) + 1), "enter the column no")
                print("hi")
                if (plr == 1):
                    col = event.pos[0]
                    col = int(np.floor(col / size))
                    human=col
                    if (validity(col)):
                        row = get_next_open_window(col)
                        put_turn(board, row, col,1)
                        win = win_cond(plr)
                        plr = (plr % 2) + 1
                        print(np.flip(board, 0))
                        game=False
                    else:
                        continue
                    if (win == 1):
                        pygame.draw.rect(screen, black, (0, 0, width, size))
                        label = myfont.render("Player 1 wins", 1, red)
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        print("player ", ((turn % 2) + 1), "WINS")
                        print(np.flip(board, 0))
                        time.sleep(2)
                        # sys.exit()
                        pygame.quit()
                        break

    return win, human


while(True):

    data=pickle.loads(s.recv(2048))
    ai=data[1]
    win=data[0]
    if(ai==-1):
        win,human=human_turn(1,win)
    else:
        if(win==1):
            row = get_next_open_window(ai)
            put_turn(board, row, ai,2)
            pygame.draw.rect(screen, black, (0, 0, width, size))
            label = myfont.render("Player 2 wins", 2, yellow)
            screen.blit(label, (40, 10))
            pygame.display.update()
            print("player  2  WINS")
            print(np.flip(board, 0))
            time.sleep(2)
            # sys.exit()
            pygame.quit()
        else:
            row = get_next_open_window(ai)
            put_turn(board, row, ai,2)
            win,human=human_turn(1,win)



    data=[win,human]
    data=pickle.dumps(data)
    s.send(data)

