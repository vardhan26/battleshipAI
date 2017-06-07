import random
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
maxprob=0
board = []
radar = []
probscore = []
neighbourscore = []
bestprob = []

def checksink(x2,y2):				
	sizeofship = board[x2][y2]
	if board[x2][y2] in ships:
		board[x2][y2]=hit
	count = 0
	nameofship = ' '
	for key,values in shipnames.iteritems():
		if [x2,y2] in values:
			nameofship = key
			break
	if nameofship == ' ':
		return 0
	for xi,yi in shipnames[nameofship]:
		if board[xi][yi] == hit:		#might need to change later
			count+=1
	if count==sizeofship:
		for xi,yi in shipnames[nameofship]:
			radar[xi][yi]=sink
		#print nameofship + " has been sunk!!!"
		ships.remove(sizeofship)
		return 1
	else:
		return 0

def hitat(x,y):
	try:
		if board[x][y] in ships:
			radar[x][y]=hit
			checksink(x,y)
			return hit
		else:
			radar[x][y]=miss
			return miss
	except IndexError:
		print "index error, x and y must lie between 0 to 9 (inclusive)"

def cleanprob():
	for i in range(SIZE):
		for j in range(SIZE):
			probscore[i][j] = 0

def nscore(x,y):
	c=0
	if x in range(SIZE) and y in range(SIZE):
		for [i,j] in [[0,1],[0,-1],[1,0],[-1,0]]:
			try:
				if radar[x+i][y+j]==sink or radar[x+i][y+j]==miss:
					c+=1
			except IndexError:
				c+=1
	return c


def findneighbourscore(x,y):
	c=0
	for [i,j] in [[0,1],[0,-1],[1,0],[-1,0]]:
		c+=nscore(x+i,y+j)
	return c

def calcprob(x,y,shipsize):	
	#horizontal
	flag = 0
	for i in range(shipsize):
		if y+i>=SIZE or radar[x][y+i]!=unguessed:
			flag = 1
			break
	if flag==0:
		for i in range(shipsize):
			probscore[x][y+i]+=1
	#vertical
	flag = 0
	for i in range(shipsize):
		if x+i>=SIZE or radar[x+i][y]!=unguessed:
			flag = 1
			break
	if flag==0:
		for i in range(shipsize):
			probscore[x+i][y]+=1

def shootdirection(way,x,y,blocks):
	#print "%d 	%d" %(x,y)
	for i in range(1,blocks+1):
		if radar[x][y]==sink:
			break
		if way == 'right':
			if hitat(x,y+i)==miss:
				break
		elif way == 'left':
			if hitat(x,y-i)==miss:
				break
		elif way == 'up':
			if hitat(x-i,y)==miss:
				break
		elif way== 'down':
			if hitat(x+i,y)==miss:
				break
	if i == 1:
		return 0
	elif radar[x][y]!=sink:
		return 1
	else:
		return 2


def placeship(shipsize, name):		#function to place ships on the board randomly
	while True:
		flag = 0
		x = random.randint(0,9)
		y = random.randint(0,9)
		if board[x][y]!=unguessed:
			continue
		orientation = random.randint(0,1)
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

def boardgenerator():
	for i in range(SIZE):
		radar.append([unguessed]*SIZE)
		board.append([unguessed]*SIZE)
		probscore.append([unguessed]*SIZE)
	#names = iter(sorted(shipnames.iteritems()))
	for i,j in zip(ships,sorted(shipnames)):
		placeship(i,j)

def nextmove():
	global maxprob
	maxprob=0
	global neighbourscore
	neighbourscore=[]
	global bestprob
	for i in range(SIZE):
		for j in range(SIZE):
			if radar[i][j] == unguessed:
				for sh in ships:
					calcprob(i,j,sh)
			if probscore[i][j]==maxprob:
				bestprob.append([i,j])
			elif probscore[i][j]>maxprob:
				bestprob = [[i,j]]
				maxprob = probscore[i][j]
	filter2 = []
	bestneighbour=0
	for [i,j] in bestprob:
		neighbourscore.append(findneighbourscore(i,j))
		if bestneighbour<max(neighbourscore):
			bestneighbour=max(neighbourscore)
			filter2 = [[i,j]]
		elif bestneighbour==max(neighbourscore):
			filter2.append([i,j])

	coords=random.choice(filter2)
	if (coords[0]+coords[1])%ships[-1]!=0:	
		for [i,j] in filter2:
			if (i+j)%ships[-1]==0:
				coords = [i,j]
				break
	cleanprob()
	return coords

def target_mode(x, y):
	direction = {'right':0,'left':0,'down':0,'up':0}
	k=1
	while y+k<SIZE and radar[x][y+k]==unguessed:
		k+=1
	direction['right']=k-1
	k=1
	while y-k>=0 and radar[x][y-k]==unguessed:
		k+=1
	direction['left']=k-1
	k=1
	while x+k<SIZE and radar[x+k][y]==unguessed:
		k+=1
	direction['down']=k-1
	k=1
	while x-k>=0 and radar[x-k][y]==unguessed:
		k+=1
	direction['up']=k-1
	DIR=' '
	while radar[x][y]!=sink:
		if (direction['right']+direction['left'])>(direction['up']+direction['down']):
			if direction['right']>direction['left']:
				DIR='right'
			else:
				DIR='left'
		#elif (direction['right']+direction['left'])<(direction['up']+direction['down']):
		else:
			if direction['up']>direction['down']:
				DIR='up'
			else:
				DIR='down'
		result = shootdirection(DIR,x,y,direction[DIR])	#shoots in the direction DIR and returns the result
		if result == 0:		#result is a miss
			direction[DIR]=0
		elif result == 1: 	#result is hits without sinking x,y and now we shoot in opposite direction of DIR
			direction[DIR]=0
			if direction.get('down',0) and DIR == 'up':
				shootdirection('down',x,y,direction['down'])
				#del direction['up']
				direction['down']=0
			elif direction.get('up',0) and DIR == 'down':
				shootdirection('up',x,y,direction['up'])
				direction['up']=0
				#del direction['down']
			elif direction.get('left',0) and DIR == 'right':
				shootdirection('left',x,y,direction['left'])
				direction['left']=0
				#del direction['right']
			elif direction.get('right',0) and DIR == 'left':
				shootdirection('right',x,y,direction['right'])
				#del direction['left']
				direction['right']=0
	del direction
	flag = 0
	for i in range(SIZE):
		for j in range(SIZE):
			if radar[i][j]==hit:
				target_mode(i,j)
				flag = 1
				break
		if flag:
			break



boardgenerator()
c=0
while True:
	x,y = nextmove()
	hitat(x,y)
	if radar[x][y]==hit:
		target_mode(x,y)
	if len(ships)==0:
		for i in range(SIZE):
			for j in range(SIZE):
				if radar[i][j] in [miss,sink]:
					c+=1
		print "victory in %d moves" %(c)
		break