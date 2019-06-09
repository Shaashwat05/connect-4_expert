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
screen_size=(width,height)
screen=pygame.display.set_mode(screen_size)
pygame.draw.rect(screen,blue,(0,size,width,(row_size*size)))
for i in range(row_size):
    for j in  range(column_size):
        pygame.draw.circle(screen,black,(int((j*size)+size/2),int(size+size/2+(i*size))),int(size/2-5))
pygame.display.update()



#checking for the validity of the move
def validity(col):
    row=row_count[col]
    if(row<row_size):
        if(board[row][col]==0):
            return True
    return False

#putting the repective player's pieces in their positions
def put_turn(col):
    plr=(turn%2)+1
    board[row_count[col],col]=plr
    if(plr==1):
        pygame.draw.circle(screen,red,(int((col)*size+size/2),int((5-row_count[col])*size+size+size/2)),int(size/2-5))
    else:
        pygame.draw.circle(screen,yellow, (int((col)*size+size/2),int((5-row_count[col])*size+size+size/2)),int(size/2-5))
    pygame.display.update()
    row_count[col]+=1

#checking win condition
def win_cond():

    plr=(turn%2)+1
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

# the game
while(game=="True" or game=="true"):
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            sys.exit()
        if(event.type==pygame.MOUSEMOTION):
            poss=event.pos[0]
            pygame.draw.rect(screen,black,(0,0,width,size))
            if(turn%2==0):
                pygame.draw.circle(screen,red,(poss,int(size/2)),int(size/2-5))
            else:
                pygame.draw.circle(screen,yellow, (poss, int(size / 2)), int(size / 2 - 5))
            pygame.display.update()

        if (event.type == pygame.MOUSEBUTTONDOWN):
            # print("player ", ((turn % 2) + 1), "enter the column no")
            col = event.pos[0]
            col = int(np.floor(col / size))
            if (validity(col)):
                put_turn(col)
                win = win_cond()
            else:
                # print("invlaid coloumn")
                # print("player ", ((turn % 2) + 1), "re-enter the column no")
                col = event.pos[0]
                col = int(np.floor(col / size))
                put_turn(col)
                win = win_cond()
            # noinspection PyUnreachableCode
            if (win == 1):
                print("player ", ((turn % 2) + 1), "WINS")
                print(np.flip(board, 0))
                sys.exit()
                # print(board)

            turn += 1
            # print(board)
            print(np.flip(board, 0))
            # print("do u want to continut the game")
            # game=input()

