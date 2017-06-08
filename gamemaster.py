import battleship as p1
import battleship2 as p2
from pprint import pprint
names=['aircraft carrier','battleship','destroyer','cruiser','patrol boat']
hit=7
miss=1
sink=9
counter=0
matches = 100
for a in range(matches):	
	p1.boardgenerator()
	p2.boardgenerator()
	while True:
		x,y = p1.nextmove()
		move = p2.hitat(x,y)
		p1.updateradar(x,y,move)
		if len(p1.ships)==0:
			counter+=1
			#print "victory in %d moves" %(c)
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
			p1.oppships = [5,4,3,3,2]
			p1.maxprob=0
			p2.board = []
			p2.radar = []
			p2.probscore = []
			p2.neighbourscore = []
			p2.bestprob = []
			p2.hitfound = []
			p2.shipnames = {'aircraft carrier':[],
						'battleship':[],
						'destroyer':[],
						'cruiser':[],
						'patrol boat':[]}
			p2.ships = [5,4,3,3,2]
			p2.oppships = [5,4,3,3,2]
			p2.maxprob=0
			break
		
		x1,y1 = p2.nextmove()
		move1 = p1.hitat(x1,y1)
		p2.updateradar(x1,y1,move1)
		if len(p2.ships)==0:
			#print "victory in %d moves" %(c)
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
			p1.oppships = [5,4,3,3,2]
			p1.maxprob=0
			p2.board = []
			p2.radar = []
			p2.probscore = []
			p2.neighbourscore = []
			p2.bestprob = []
			p2.hitfound = []
			p2.shipnames = {'aircraft carrier':[],
						'battleship':[],
						'destroyer':[],
						'cruiser':[],
						'patrol boat':[]}
			p2.ships = [5,4,3,3,2]
			p2.oppships = [5,4,3,3,2]
			p2.maxprob=0
			break
	
print "player 1 won %d out of %d matches" %(counter,matches)
