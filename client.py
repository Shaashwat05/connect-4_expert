import socket
import os
import subprocess
import pygame
import numpy as np
import sys
import random
import time
import math



pygame.init()




#global variables
row_size=6
column_size=7
board=np.zeros((row_size,column_size))
np.flip(board,0)
game="True"
turn=0
plr=(turn%2)+1
row_count=[0,0,0,0,0,0,0]
win=0
size=100
height=int((row_size+1)*size)
width=int(column_size*size)
blue=(0,0,255)
black=(0,0,0)
red=(255,0,0)
yellow=(255,255,0)
plr=random.randint(1,2)
myfont = pygame.font.SysFont("monospace", 75)



s=socket.socket()
host="192.168.1.100"
port=9999

s.connect((host,port))









#creating the screen of the game
screen_size=(width,height)
screen=pygame.display.set_mode(screen_size)
pygame.draw.rect(screen,blue,(0,size,width,(row_size*size)))
for i in range(row_size):
    for j in  range(column_size):
        pygame.draw.circle(screen,black,(int((j*size)+size/2),int(size+size/2+(i*size))),int(size/2-5))
pygame.display.update()



#checking for the validity of the move
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



def put_turn2(board2,row,col,plr):
    board2[row,col]=plr


def get_valid_locations():
    valid_locations=[]
    for i in range(column_size):
        if (validity(i)):
            valid_locations.append(i)
    return valid_locations









# the game

def plr1_turn(s):
    while(game=="True" or game=="true"):
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                #sys.exit()
                pygame.quit()
            if(event.type==pygame.MOUSEMOTION):
                poss=event.pos[0]
                pygame.draw.rect(screen,black,(0,0,width,size))
                pygame.draw.circle(screen,red,(poss,int(size/2)),int(size/2-5))
                pygame.display.update()

            if (event.type == pygame.MOUSEBUTTONDOWN):
                # print("player ", ((turn % 2) + 1), "enter the column no")
                col = event.pos[0]
                col = int(np.floor(col / size))
                plr=1
                if (validity(col)):
                    row=get_next_open_window(col)
                    put_turn(board,row,col,plr)
                    win = win_cond(1)
                    print(np.flip(board, 0))
                    plr=(plr%2)+1
                else:
                    continue
                if (win == 1):
                    pygame.draw.rect(screen, black, (0, 0, width, size))
                    label = myfont.render("Player 1 wins", 1, red)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    print("player  1 WINS")
                    print(np.flip(board, 0))
                    time.sleep(2)
                    pygame.quit()
                col=str(col)
                s.send(str.encode(col))







while True:
    x = s.recv(1024)
    x=x.decode("utf-8")
    col=int(x)
    if(col!=-1):
        plr = 2
        if (validity(col)):

            row = get_next_open_window(col)
            put_turn(board, row, col,plr)
            win = win_cond(2)
            print(np.flip(board, 0))
            plr=(plr%2)+1
            if (win == 1):
                pygame.draw.rect(screen, black, (0, 0, width, size))
                label = myfont.render("Player 2 wins", 2, yellow)
                screen.blit(label, (40, 10))
                pygame.display.update()
                print("player 2 WINS")
                print(np.flip(board, 0))
                time.sleep(2)
                pygame.quit()
                #sys.exit()
            else:
                plr1_turn(s)
    else:
        plr1_turn(s)























