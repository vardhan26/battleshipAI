import random
from pprint import pprint
from copy import deepcopy
import numpy as np

shipnames = {'aircraft carrier':[],
			'battleship':[],
			'destroyer':[],
			'cruiser':[],
			'patrol boat':[]}
ships = [5,4,3,3,2]
oppships=[5,4,3,3,2]
unguessed = 0
miss = 1
hit = 7
checkeredpattern=0
sink = 9
SIZE = 10
scoreadd=100
dispersion=0.000
maxprob=0
matchcount=0
board = []
radar = []
probscore = []
neighbourscore = []
bestprob = []
hitfound = []
oppstatscore = np.zeros((10,10),dtype=int)
statscore = []
for i in range(SIZE):
	statscore.append([0]*SIZE)

def resetplayer(self):
	self.board = []
	self.radar = []
	self.probscore = []
	self.neighbourscore = []
	self.bestprob = []
	self.hitfound = []
	self.shipnames = {'aircraft carrier':[],
				'battleship':[],
				'destroyer':[],
				'cruiser':[],
				'patrol boat':[]}
	self.ships = [5,4,3,3,2]
	self.oppships = [5,4,3,3,2]
	self.scoreadd = 100
	self.maxprob=0
	self.checkeredpattern=random.randint(0,1)


def checksink(x2,y2):				
	tosink = []
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
			tosink.append([xi,yi])
		#print nameofship + " has been sunk!!!"
		ships.remove(sizeofship)
		return tosink
	else:
		return 0


def updateradar(x,y,state):
	global hitfound
	try:	
		if state == hit or state==miss:
			radar[x][y]=state
			if state==hit:
				oppstatscore[x][y]+=1
				hitfound.append([x,y])
			else:
				oppstatscore[x][y]-=2
				#print x,y
		else:
			oppstatscore[x][y]+=1
			for [xi,yi] in state:
				radar[xi][yi]=sink
				if [xi,yi] in hitfound:
					hitfound.remove([xi,yi])
			oppships.remove(len(state))
	except TypeError:
		print "not an applicable state"


def hitat(x,y):
	global scoreadd
	global statscore
	try:
		statscore[x][y]+=scoreadd
		scoreadd-=1
		statscore[x][y]=int((statscore[x][y])/2)
		if board[x][y] in ships:
			sinker = checksink(x,y)
			if sinker!=0:
				return sinker
			return hit
		else:
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

def calcprob(x,y,shipsize):		#try the hitfound append thing
	if len(hitfound)!=0:
		for [xi,yi] in hitfound:
			if y==yi:
				f=0
				if x<=xi and x+shipsize-1>=xi and x+shipsize-1<SIZE:
					for i in range(shipsize):
						if radar[x+i][y] not in [hit,unguessed]:
							f=1
							break
					if f==0:
						for i in range(shipsize):
							if radar[x+i][y]==unguessed:
								probscore[x+i][y]+=1
			if x==xi:
				f=0
				if y<=yi and y+shipsize-1>=yi and y+shipsize-1<SIZE:
					for i in range(shipsize):
						if radar[x][y+i] not in [hit,unguessed]:
							f=1
							break
					if f==0:
						for i in range(shipsize):
							if radar[x][y+i]==unguessed:
								probscore[x][y+i]+=1



	else:
		#horizontal
		flag = 0
		for i in range(shipsize):
			if y+i>=SIZE or radar[x][y+i]!=unguessed:
				flag = 1
				break
		if flag==0:
			for i in range(shipsize):
				if radar[x][y+i]==unguessed:
					probscore[x][y+i]+=1
		#vertical
		flag = 0
		for i in range(shipsize):
			if x+i>=SIZE or radar[x+i][y]!=unguessed:
				flag = 1
				break
		if flag==0:
			for i in range(shipsize):
				if radar[x+i][y]==unguessed:
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
	flag = 0
	orientation = 0
	maxscore =100
	curscore1,curscore2 = 0,0
	bestpos = []
	curpos1 = []
	curpos2 = []
	# x = random.randint(0,9)
	# y = random.randint(0,9)
	# if board[x][y]!=unguessed:
	# 	continue
	# orientation = random.randint(0,1)
	# if orientation:
	# 	for i in range(shipsize):
	# 		if y+i>=SIZE or board[x][y+i]!=unguessed:
	# 			flag = 1
	# 			break
	# else:
	# 	for i in range(shipsize):
	# 		if x+i>=SIZE or board[x+i][y]!=unguessed:
	# 			flag = 1
	# 			break
	for i in range(SIZE):
		for j in range(SIZE):
			for k in range(shipsize):
				curpos1.append([i,j+k])
				if j+k>=SIZE or board[i][j+k]!=unguessed:
					curscore1 = 0
					flag+=1
					curpos1 = []
					break
				if statscore[i][j+k]>=curscore1:
					curscore1 = statscore[i][j+k]
			for k in range(shipsize):
				curpos2.append([i+k,j])
				if i+k>=SIZE or board[i+k][j]!=unguessed:
					curscore2 = 0
					flag+=1
					curpos2 = []
					break
				if statscore[i+k][j]>=curscore2:
					curscore2 = statscore[i+k][j]
			if flag<2:
				if curscore1>min(curscore2,curscore1):
					if len(curpos2)>0:	
						curpos1 = curpos2
						curscore1 = curscore2
				elif len(curpos1)==0:
					curpos1=curpos2
					curscore1=curscore2
				if curscore1<=maxscore:
					maxscore = curscore1
					bestpos = curpos1
			flag=0
			curscore1,curscore2 = 0,0
			curpos1,curpos2 = [],[]
	#print bestpos
	for i in range(shipsize):
		board[bestpos[i][0]][bestpos[i][1]]=shipsize
	shipnames[name] = shipnames[name] + bestpos




def boardgenerator():
	global oppstatscore,dispersion,matchcount
	matchcount+=1
	if matchcount%100==0:
		oppstatscore=oppstatscore/5
	for i in range(SIZE):
		radar.append([unguessed]*SIZE)
		board.append([unguessed]*SIZE)
		probscore.append([unguessed]*SIZE)
	#names = iter(sorted(shipnames.iteritems()))
	for i,j in zip(ships,sorted(shipnames)):
		placeship(i,j)
	v = np.var(oppstatscore)
	#print v
	mean = np.mean(oppstatscore)
	#print mean
	try:
		dispersion = v/(mean*mean)
		print dispersion
	except ZeroDivisionError:
		dispersion=0
	oppstatscore=oppstatscore+np.ones((SIZE,SIZE),dtype=int)
	pprint(oppstatscore)
	#pprint(board)

def bestml():
	maxstat=-250
	beststat=[]
	for i in range(SIZE):
		for j in range(SIZE):
			if radar[i][j]!=unguessed:
				continue
			if oppstatscore[i][j]>maxstat:
				maxstat=oppstatscore[i][j]
				beststat = [[i,j]]
			elif oppstatscore[i][j]==maxstat:
				beststat.append([i,j])
	return random.choice(beststat)

def nextmove():
	global maxprob,checkeredpattern
	maxprob=0
	global neighbourscore
	neighbourscore=[]
	coords=[]
	global bestprob
	for i in range(SIZE):
		for j in range(SIZE):
			if radar[i][j] == unguessed or radar[i][j]==hit:
				for sh in oppships:
					calcprob(i,j,sh)
			if probscore[i][j]==maxprob:
				bestprob.append([i,j])
			elif probscore[i][j]>maxprob:
				bestprob = [[i,j]]
				maxprob = probscore[i][j]
	random.shuffle(bestprob)
	if len(hitfound)==0:	
		if dispersion>0.7 and matchcount>75:
				coords = bestml()
				return coords
		filter2 = []
		bestneighbour=0
		for [i,j] in bestprob:
			neighbourscore.append(findneighbourscore(i,j))
			if bestneighbour<max(neighbourscore):
				bestneighbour=max(neighbourscore)
				filter2 = [[i,j]]
			elif bestneighbour==max(neighbourscore):
				filter2.append([i,j])
		random.shuffle(filter2)
		coords=random.choice(filter2)
		if (coords[0]+coords[1])%oppships[-1]!=checkeredpattern:
			for [i,j] in filter2:
				if (i+j)%oppships[-1]==checkeredpattern:
					coords = [i,j]
					break
	else:
		#pprint(probscore)
		#input()
		if len(hitfound)==1:
			coords = random.choice(bestprob)
		else:
			if hitfound[-1][0]==hitfound[0][0]:
				x1=hitfound[0][0]
				y1=probscore[hitfound[0][0]].index(max(probscore[hitfound[0][0]]))
				if probscore[x1][y1]!=0:
					coords = [x1,y1]
				else:
					for [i,j] in bestprob:
						if j==hitfound[0][1]:
							coords=[i,j]
							break
			if hitfound[-1][1]==hitfound[0][1]:
				y1=hitfound[0][1]
				x1=0
				maxx=0
				for i in range(SIZE):
					if maxx<probscore[i][y1]:
						x1=i
						maxx=probscore[i][y1]
				if probscore[x1][y1]!=0:
					coords = [x1,y1]
				else:
					for [i,j] in bestprob:
						if i==hitfound[0][0]:
							coords=[i,j]
							break
						
	if len(coords)==0:
		coords=random.choice(bestprob)
	#print coords
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