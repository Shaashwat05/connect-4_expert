import pygame
import sys
import numpy as np
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

#creating the screen of the game
screen_size=(width,height)
screen=pygame.display.set_mode(screen_size)
pygame.draw.rect(screen,blue,(0,size,width,(row_size*size)))
for i in range(row_size):
    for j in  range(column_size):
        pygame.draw.circle(screen,black,(int((j*size)+size/2),int(size+size/2+(i*size))),int(size/2-5))
pygame.display.set_caption("ai ")
pygame.display.update()

#checking for the validity of the move
def validity(col):
    return board[row_size-1][col]==0


def get_next_open_window(col):
    for r in range(row_size):
        if board[r][col] == 0:
            return r
        

#putting the repective player's pieces in their positions
def put_turn(board,row,col):
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


def cal_score(window):
    score=0
    if(window.count(2)==4):
        score+=100
    elif(window.count(2) == 3 and window.count(0) == 1):
        score += 5
    elif(window.count(2) == 2 and window.count(0) == 2):
        score+=2
    elif(window.count(1) == 3 and window.count(0) == 1):
        score-=8
    elif (window.count(1) == 2 and window.count(0) == 2):
        score -= 12
    return score



def score_position(board):
    score = 0


    center_array=[int(i) for i in list(board[:,column_size//2])]
    countt=center_array.count(2)
    score+=(countt*6)+6


    for i in range(row_size):
        r_array = [int(k) for k in list(board[i, :])]
        for j in range(column_size-3):
            window = r_array[j:j + 4]
            score+=cal_score(window)


    for i in range(column_size):
        c_array=[int(k) for k in list(board[:,i])]
        for j in range(row_size-3):
            window=c_array[j:j+4]
            score+=cal_score(window)

    for i in range(row_size-3):
        for j in range(column_size-3):
            window=[board[i+k][j+k] for k in range(4)]
            score+=cal_score(window)


    for i in range(row_size-3):
        for j in range(column_size-3):
            window =[board[i+3-k][j+k] for k in range(4)]
            score+=cal_score(window)


    return score
def put_turn2(board2,row,col,plr):
    board2[row,col]=plr


def get_valid_locations():
    valid_locations=[]
    for i in range(column_size):
        if (validity(i)):
            valid_locations.append(i)
    return valid_locations


def is_terminal_node():
    return win_cond(1) or win_cond(2) or len(get_valid_locations())==0


def minimax(board,depth,alpha,beta,maximizingPlayer):

    valid_locations=get_valid_locations()
    is_terminal=is_terminal_node()
    if(depth==0 or is_terminal):
        if(is_terminal):
            if (win_cond(2)):
                return (None, 100000000)
            elif (win_cond(1)):
                return (None, -100000000)
            else:
                return (None, 0)
        else:
            return (None,score_position(board))

    if maximizingPlayer==True:
        value=-math.inf
        column=random.choice(valid_locations)
        for c in valid_locations:
            row=get_next_open_window(c)
            b_copy=board.copy()
            put_turn2(b_copy,row,c,2)
            new_score=minimax(b_copy,depth-1,alpha,beta,False)[1]
            if(new_score>value):
                value=new_score
                column=c
            alpha=max(alpha,value)
            if(alpha>=beta):
                break
        return column,value
    else:
        value = math.inf
        column=random.choice(valid_locations)
        for c in valid_locations:
            row =get_next_open_window(c)
            b_copy = board.copy()
            put_turn2(b_copy, row, c,1)
            new_score =  minimax(b_copy, depth - 1,alpha,beta, True)[1]
            if(new_score<value):
                value=new_score
                column=c
            beta=min(beta,value)
            if(alpha>=beta):
                break
        return column,value


# THE GAME
plr=random.randint(1,2)
myfont = pygame.font.SysFont("monospace", 75)

while(game=="True" or game=="true"):
    for event in pygame.event.get():

        if(event.type==pygame.QUIT):
            pygame.quit()
            #sys.exit()
        if(event.type==pygame.MOUSEMOTION):
            poss=event.pos[0]
            pygame.draw.rect(screen,black,(0,0,width,size))
            if(plr==1):
                pygame.draw.circle(screen,red,(poss,int(size/2)),int(size/2-5))
            pygame.display.update()

        if (event.type == pygame.MOUSEBUTTONDOWN):
            # print("player ", ((turn % 2) + 1), "enter the column no")
            print("hi")
            if(plr==1):
                col = event.pos[0]
                col = int(np.floor(col / size))
                if (validity(col)):
                    row=get_next_open_window(col)
                    put_turn(board,row,col)
                    win = win_cond(plr)
                    plr=(plr%2)+1
                    print(np.flip(board, 0))
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
                    #sys.exit()
                    pygame.quit()

    if(plr==2):
        col,minimax_score=minimax(board,5,-math.inf,math.inf,True)
        #print(minimax_score)
        if(validity(col)):
            row=get_next_open_window(col)
            put_turn(board,row,col)
            win=win_cond(plr)
            plr=(plr%2)+1
            print(np.flip(board, 0))
            if (win == 1):
                pygame.draw.rect(screen, black, (0, 0, width, size))
                label = myfont.render("Player 2 wins", 2, yellow)
                screen.blit(label, (40, 10))
                pygame.display.update()
                print("player ", ((turn % 2) + 1), "WINS")
                print(np.flip(board, 0))
                time.sleep(2)
                #sys.exit()
                pygame.quit()





