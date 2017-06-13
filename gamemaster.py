import battleship as p1
import battleship2 as p2
from pprint import pprint
import pygame,sys
from pygame.locals import *
FPS = 30

windowwidth = 1280
windowheight = 720
revealspeed = 8
boxsize = 40
gapsize = 5
boardgap = 20
boardwidth = 10
boardheight = 10
assert (boardwidth*boardheight)%2==0, "we need even no. of boxes"
xmargin = int((windowwidth-(boardgap+(boardwidth*(boxsize+gapsize)*2)))/2)
ymargin = int((windowheight-(boardheight*(boxsize+gapsize)))/2)


gray = (100,100,100)
navyblue = (60,60,100)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
orange = (255,128,0)
purple = (255,0,255)
cyan = (0,255,255)
black = (15,15,15)

bgcolor = navyblue
lightbgcolor = gray
boxcolor = white
highlightcolor = blue


names=['aircraft carrier','battleship','destroyer','cruiser','patrol boat']
hit=7
miss=1
sink=9
unguessed=0
matches = 10



def main():
	p1.boardgenerator()
	p2.boardgenerator()

	global FPSCLOCK,DISPLAYSURF
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF=pygame.display.set_mode((windowwidth,windowheight))

	pygame.display.set_caption('BATTLESHIP')
	DISPLAYSURF.fill(bgcolor)
	counter = 0
	abc=0
	noofmoves=0

	while True:
		noofmoves+=1
		DISPLAYSURF.fill(bgcolor)
		drawRadar(p1.radar,p2.radar)

		if abc>=matches:
			print "player 2 won %d out of %d matches" %(counter,matches)
			pygame.quit()
			sys.exit()

		for event in pygame.event.get():
			if event.type == QUIT or (event.type==KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()

		x,y = p1.nextmove()
		move = p2.hitat(x,y)
		p1.updateradar(x,y,move)
		if len(p1.ships)==0:
			#print "victory in %d moves" %(c)
			pprint(p1.statscore)
			counter+=1
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
			p1.scoreadd = 100
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
			if abc>=matches:
				print "player 1 won %d out of %d matches" %(counter,matches)
				pygame.quit()
				sys.exit()
			else:
				abc+=1
				print noofmoves
				noofmoves=0
				p1.boardgenerator()
				p2.boardgenerator()

		
		x1,y1 = p2.nextmove()
		move1 = p1.hitat(x1,y1)
		p2.updateradar(x1,y1,move1)
		if len(p2.ships)==0:
			#print "victory in %d moves" %(c)
			pprint(p1.statscore)
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
			p1.scoreadd = 100
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
			if abc>=matches:
				print "player 1 won %d out of %d matches" %(counter,matches)
				pygame.quit()
				sys.exit()
			else:
				abc+=1
				print noofmoves
				noofmoves=0
				p1.boardgenerator()
				p2.boardgenerator()

		pygame.display.update()
		FPSCLOCK.tick(FPS)

def leftTopCoordsOfBox(boxx,boxy):
	left = boxx*(boxsize+gapsize) + xmargin
	top = boxy*(boxsize+gapsize) + ymargin
	return (left,top)

def drawRadar(radar1,radar2):
	for x in range(boardwidth):
		for y in range(boardheight):
			left,top = leftTopCoordsOfBox(x,y)
			if radar1[y][x] == unguessed:
				pygame.draw.rect(DISPLAYSURF,white,(left,top,boxsize,boxsize))
			elif radar1[y][x] == hit:
				pygame.draw.rect(DISPLAYSURF,red,(left,top,boxsize,boxsize))
			elif radar1[y][x] == miss:
				pygame.draw.rect(DISPLAYSURF,blue,(left,top,boxsize,boxsize))
			elif radar1[y][x] == sink:
				pygame.draw.rect(DISPLAYSURF,black,(left,top,boxsize,boxsize))
			left = left + boardwidth*(boxsize+gapsize) + boardgap
			if radar2[y][x] == unguessed:
				pygame.draw.rect(DISPLAYSURF,white,(left,top,boxsize,boxsize))
			elif radar2[y][x] == hit:
				pygame.draw.rect(DISPLAYSURF,red,(left,top,boxsize,boxsize))
			elif radar2[y][x] == miss:
				pygame.draw.rect(DISPLAYSURF,blue,(left,top,boxsize,boxsize))
			elif radar2[y][x] == sink:
				pygame.draw.rect(DISPLAYSURF,black,(left,top,boxsize,boxsize))

if __name__ == '__main__':
		main()


