import battleship as p1

names=['aircraft carrier','battleship','destroyer','cruiser','patrol boat']
hit=7
miss=1
sink=9
counter=0
for a in range(10000):	
	p1.boardgenerator()
	c=0
	while True:
		x,y = p1.nextmove()
		move = p1.hitat(x,y)
		p1.updateradar(x,y,move)
		if len(p1.ships)==0:
			for i in range(p1.SIZE):
				for j in range(p1.SIZE):
					if p1.radar[i][j] in [p1.miss,p1.sink]:
						c+=1
			#print "victory in %d moves" %(c)
			counter+=c
			p1.board = []
			p1.radar = []
			p1.probscore = []
			p1.neighbourscore = []
			p1.bestprob = []
			p1.hitfound = []
			p1.shipnames = {'aircraft carrier':[],
						'battleship':[],
						'destroyer':[],
						'cruiser':[],
						'patrol boat':[]}
			p1.ships = [5,4,3,3,2]
			p1.maxprob=0
			break
	
print float(counter)/10000
