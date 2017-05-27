#battleship
#initialise everything
from random import randint
from pprint import pprint
from copy import deepcopy
shipnames = {'aircraft carrier':[],
		'battleship':[],
		'destroyer':[],
		'cruiser':[],
		'patrol boat':[]}

ships = [5,4,3,3,2]
unguessed = 0
miss = 1
hit = 7
sink = 9
SIZE = 10
board = []
static_board = []
shootable = [unguessed]
for i in ships:
	shootable.append(i)

def placeship(shipsize, name):		#function to place ships on the board randomly
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
					shipnames[name] = shipnames[name] + [[x,y+i]]
			else:
				for i in range(shipsize):
					board[x+i][y] = shipsize
					shipnames[name] = shipnames[name] + [[x+i,y]]
			break

def checksink(x1,y1,x2,y2):				
	sizeofship = static_board[x2][y2]
	count = 0
	nameofship = ' '
	for key,values in shipnames.iteritems():
		if [x2,y2] in values:
			nameofship = key
			break
	if nameofship == ' ':
		return 0
	for xi,yi in shipnames[nameofship]:
		if board[xi][yi] == hit:
			count+=1
	if count==sizeofship:
		for xi,yi in shipnames[nameofship]:
			board[xi][yi]=sink
		#print nameofship + " has been sunk!!!"
		ships.remove(sizeofship)
		return 1
	else:
		return 0


def shootdirection(way,x,y,blocks):
	#print "%d 	%d" %(x,y)
	if y+1<SIZE and way == 'right':
		if board[x][y+1]==unguessed:
			board[x][y+1] = miss
			return 0
		else:
			board[x][y+1] = hit
			if not checksink(x,y,x,y+1):		
				for i in range(2,blocks+1):
					if static_board[x][y+i] in ships:
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
	elif y-1>=0 and way == 'left':
		if board[x][y-1]==unguessed:
			board[x][y-1] = miss
			return 0
		else:
			board[x][y-1] = hit
			if not checksink(x,y,x,y-1):		
				for i in range(2,blocks+1):
					if static_board[x][y-i] in ships:
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
	elif x+1<SIZE and way == 'down':
		if board[x+1][y]==unguessed:
			board[x+1][y] = miss
			return 0
		else:
			board[x+1][y] = hit
			if not checksink(x,y,x+1,y):		
				for i in range(2,blocks+1):
					if static_board[x+i][y] in ships:
						board[x+i][y]=hit
						if checksink(x,y,x+i,y):
							break
					else:
						board[x+i][y] = miss
						break
			else:
				return 2
			if board[x][y] == hit:
				return 1
	elif x-1>=0 and way == 'up':
		if board[x-1][y]==unguessed:
			board[x-1][y] = miss
			return 0
		else:
			board[x-1][y] = hit
			if not checksink(x,y,x-1,y):		
				for i in range(2,blocks+1):
					if static_board[x-i][y] in ships:
						board[x-i][y]=hit
						if checksink(x,y,x-i,y):
							break
					else:
						board[x-i][y] = miss
						break
			else:
				return 2
			if board[x][y] == hit:
				return 1
	else:
		return 0

def target_mode(x, y):
	direction = {'right':0,'left':0,'down':0,'up':0}		#directions from x,y
	k=1
	while y+k<SIZE and board[x][y+k] in shootable:
		k+=1
	direction['right']=k-1
	k=1
	while y-k>=0 and board[x][y-k] in shootable:
		k+=1
	direction['left']=k-1
	k=1
	while x+k<SIZE and board[x+k][y] in shootable:
		k+=1
	direction['down']=k-1
	k=1
	while x-k>=0 and board[x-k][y] in shootable:
		k+=1
	direction['up']=k-1
	while board[x][y]!=sink:
		#pprint(board)
		#print direction
		#print "%d 	%d" %(x,y)
		DIR = max(direction, key=direction.get)
		#print DIR
		result = shootdirection(DIR,x,y,direction[DIR])	#shoots in the direction DIR and returns the result
		if result == 0:		#result is a miss
			del direction[DIR]
		elif result == 1: 	#result is hits without sinking x,y and now we shoot in opposite direction of DIR
			del direction[DIR]
			if direction.get('down',0) and DIR == 'up':
				shootdirection('down',x,y,direction['down'])
				#del direction['up']
				del direction['down']
			elif direction.get('up',0) and DIR == 'down':
				shootdirection('up',x,y,direction['up'])
				del direction['up']
				#del direction['down']
			elif direction.get('left',0) and DIR == 'right':
				shootdirection('left',x,y,direction['left'])
				del direction['left']
				#del direction['right']
			elif direction.get('right',0) and DIR == 'left':
				shootdirection('right',x,y,direction['right'])
				#del direction['left']
				del direction['right']
	flag = 0
	for i in range(SIZE):
		for j in range(SIZE):
			if board[i][j]==hit:
				target_mode(i,j)
				flag = 1
				break
		if flag:
			break
	
#generate a board
for i in range(SIZE):
	board.append([unguessed]*SIZE)
names = iter(sorted(shipnames.iteritems()))
for i,j in zip(ships,sorted(shipnames)):
	placeship(i,j)
#pprint(board)
static_board = deepcopy(board)
counter=0
while True:
	x = randint(0,9)
	y = randint(0,9)
	if board[x][y] not in shootable or (x+y)%ships[-1]!=0:		#use of parity concept and random shooting till a hit is found
		continue
	if board[x][y] in ships:
		board[x][y]=hit
		target_mode(x,y)
	else:
		board[x][y]=miss
	if len(ships)==0:
		#pprint(board)
		for i in range(SIZE):
			for j in range(SIZE):
				if board[i][j]==1:
					counter+=1
		print counter+17
		break
