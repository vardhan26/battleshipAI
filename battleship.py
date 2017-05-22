#battleship
#initialise everything
from random import randint
from pprint import pprint
from copy import deepcopy
shipnames = {'carrier':5,
		'battleship':4,
		'destroyer':3,
		'cruiser':3,
		'boat':2}
ships = [5,4,3,3,2]
unguessed = 0
miss = 1
hit = -1
sink = -2
SIZE = 10
board = []
static_board = []
shootable = [unguessed]
for i in ships:
	shootable.append(i)

def placeship(shipsize):		#function to place ships on the board randomly
	while True:
		flag = 0
		x = randint(0,9)
		y = randint(0,9)
		if board[x][y]!=unguessed:
			continue
		orientation = randint(0,1)
		if orientation:
			for i in range(shipsize):
				if y+i>=SIZE or board[x][y+i]!=unguessed:
					flag = 1
					break
		else:
			for i in range(shipsize):
				if x+i>=SIZE or board[x+i][y]!=unguessed:
					flag = 1
					break
		if not flag:
			if orientation:
				for i in range(shipsize):
					board[x][y+i] = shipsize
			else:
				for i in range(shipsize):
					board[x+i][y] = shipsize
			break


def shootdirection(way,x,y,blocks):
	if way == 0:
		if board[x][y+1]==unguessed:
			board[x][y+1] = miss
			return 0
		else:
			board[x][y+1] = hit
			if not checksink(x,y,x,y+1):		#TODO make a function checksink to check sinking status of any ship after the last hit
				for i in range(2,blocks):
					if board[x][y+i] in ships:
						board[x][y+i]=hit
						if checksink(x,y,x,y+i):
							break
					else:
						board[x][y+i] = miss
						break
			else:
				return 2
			if board[x][y] == hit:
				return 1
	if way == 1:
		if board[x][y-1]==unguessed:
			board[x][y-1] = miss
			return 0
		else:
			board[x][y-1] = hit
			if not checksink(x,y,x,y-1):		
				for i in range(2,blocks):
					if board[x][y-i] in ships:
						board[x][y-i]=hit
						if checksink(x,y,x,y-i):
							break
					else:
						board[x][y-i] = miss
						break
			else:
				return 2
			if board[x][y] == hit:
				return 1
	if way == 2:
		if board[x+1][y]==unguessed:
			board[x+1][y] = miss
			return 0
		else:
			board[x+1][y] = hit
			if not checksink(x,y,x+1,y):		
				for i in range(2,blocks):
					if board[x+1][y] in ships:
						board[x+1][y]=hit
						if checksink(x,y,x+1,y):
							break
					else:
						board[x+i][y] = miss
						break
			else:
				return 2
			if board[x][y] == hit:
				return 1
	if way == 3:
		if board[x-1][y]==unguessed:
			board[x-1][y] = miss
			return 0
		else:
			board[x-1][y] = hit
			if not checksink(x,y,x-1,y):		
				for i in range(2,blocks):
					if board[x-1][y] in ships:
						board[x-1][y]=hit
						if checksink(x,y,x-1,y):
							break
					else:
						board[x-i][y] = miss
						break
			else:
				return 2
			if board[x][y] == hit:
				return 1





def target_mode(x, y):
	direction = [0,0,0,0] 		#directions from x,y
	k=1
	while y+k<SIZE and board[x][y+k] in shootable:
		k+=1
	direction[0]=k-1
	k=1
	while y-k>=0 and board[x][y-k] in shootable:
		k+=1
	direction[1]=k-1
	k=1
	while x+k<SIZE and board[x+k][y] in shootable:
		k+=1
	direction[2]=k-1
	k=1
	while x-k>=0 and board[x-k][y] in shootable:
		k+=1
	direction[3]=k-1
	while board[x][y]!=sink:
		DIR = direction.index(max(direction))
		result = shootdirection(DIR,x,y,direction[DIR])	#shoots in the direction DIR and returns the result
		if result == 0:		#result is a miss
			del direction[DIR]
		elif result == 1: 	#result is hits without sinking x,y and now we shoot in opposite direction of DIR
			if DIR%2==0:
				shootdirection(DIR+1,x,y,direction[DIR+1])
				del direction[DIR]
				del direction[DIR]
			else:
				shootdirection(DIR-1,x,y,direction[DIR-1])
				del direction[DIR]
				del direction[DIR-1]
	if board[x+1][y]==hit:		#if any hit is found after sinking ship with x,y as a coordinate then we target that
		target_mode(x+1,y)
	elif board[x-1][y]==hit:
		target_mode(x-1,y)
	elif board[x][y+1]==hit:
		target_mode(x,y+1)
	elif board[x][y-1]==hit:
		target_mode(x,y-1)



	


#generate a board
for i in range(SIZE):
	board.append([unguessed]*SIZE)
for j in ships:
	placeship(j)
pprint(board)
static_board = deepcopy(board)

c = 0
life =17
while True:
	x = randint(0,9)
	y = randint(0,9)
	if board[x][y] not in shootable: or (x+y)%ships[-1]!=0:		#use of parity concept and random shooting till a hit is found
		continue
	c+=1
	if board[x][y] in ships:
		board[x][y]=hit
		life-=1
		target_mode(x,y)
	else:
		board[x][y]=miss
	if len(ships)==0 or life==0:
		pprint(board)
		print c
		break
	

