import pygame
import sys
import numpy as np
import math

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
EMPTY=0
WINDOW_LENGTH=4


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


def evaluate_window(window):
	score = 0
	piece=2
	opp_piece=1

	if window.count(piece) == 4:
		score += 100
	if window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	if window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2
	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, column_size//2])]
	center_count = center_array.count(2)
	score += center_count * 3

	## Score Horizontal
	for r in range(row_size):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(column_size-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window)

	## Score Vertical
	for c in range(column_size):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(row_size-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window)

	## Score posiive sloped diagonal
	for r in range(row_size-3):
		for c in range(column_size-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window)

	for r in range(row_size-3):
	for c in range(column_size-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window)

	return score



#the minimax algorithm
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board):
                return (None, 100000000000000)
            elif winning_move(board):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            put_turn(col)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            put_turn(col)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# the game
while(game=="True" or game=="true"):
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            sys.exit()
        if(event.type==pygame.MOUSEMOTION):
            poss=event.pos[0]
            pygame.draw.rect(screen,black,(0,0,width,size))
            pygame.draw.circle(screen, red, (poss, int(size / 2)), int(size / 2 - 5))
            pygame.display.update()

        if(((turn%2)+1)==1):
            if (event.type == pygame.MOUSEBUTTONDOWN):
                # print("player ", ((turn % 2) + 1), "enter the column no")
                col = event.pos[0]
                col = int(np.floor(col / size))

        else:
            col,minimax_score=minimax(board, 5, -math.inf, math.inf, True)

        if(validity(col)):
            put_turn(col)
            win=win_cond()
        else:
        continue
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

