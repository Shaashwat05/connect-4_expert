import socket
import sys
import random
import pygame
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

#creating the screen of the game
screen_size=(width,height)
screen=pygame.display.set_mode(screen_size)
pygame.draw.rect(screen,blue,(0,size,width,(row_size*size)))
for i in range(row_size):
    for j in  range(column_size):
        pygame.draw.circle(screen,black,(int((j*size)+size/2),int(size+size/2+(i*size))),int(size/2-5))
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

def create_socket():
    try:
        global host
        global s
        global port
        host=""
        port=9999
        s=socket.socket()
    except socket.error as mag:
        print("socket creation error",str(mag))


def bind_socket():
    try:
        global host
        global s
        global port

        print("binding the socket")
        s.bind((host,port))
        s.listen(5)


    except socket.error as mag:
        print("socket binding error ",str(mag)," retrying")
        bind_socket()


def accept():
    conn,adress=s.accept()
    conn.setblocking(1)
    print("ip : ",adress[0]," port : ",adress[1])
    send_command(conn)
    conn.close()




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





def ai_turn(plr):
    print("ai")
    col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
    # print(minimax_score)
    if (validity(col)):
        print("hi")
        row = get_next_open_window(col)
        put_turn(board, row, col,2)
        win = win_cond(plr)
        plr = (plr % 2) + 1
        print(np.flip(board, 0))
        if (win == 1):
            pygame.draw.rect(screen, black, (0, 0, width, size))
            label = myfont.render("Player 2 wins", 2, yellow)
            screen.blit(label, (40, 10))
            pygame.display.update()
            print("player 2 WINS")
            print(np.flip(board, 0))
            time.sleep(2)
            # sys.exit()
            pygame.quit()
    return win,col

def send_command(conn):
    while True:
        cmd=input()
        if(cmd=="quit"):
            conn.close()
            s.close()
            sys.exit()
        if(cmd=="start"):
            plr=random.randint(1,2)
            ai=-1
            win=0
            game=True
            while game:
                data = [win, ai]
                conn.send(pickle.dumps(data))
                data=pickle.loads(conn.recv(2048))
                human=data[1]
                win=data[0]
                row = get_next_open_window(human)
                put_turn(board, row, human,1)
                if win == 0:
                    win,ai=ai_turn(2)








def main():
    create_socket()
    bind_socket()
    accept()

main()

