import battleship as p1

p1.boardgenerator()
c=0
while True:
	try:
		x,y = p1.nextmove()
		p1.hitat(x,y)
		if p1.radar[x][y]==p1.hit:
			p1.target_mode(x,y)
		if len(p1.ships)==0:
			for i in range(p1.SIZE):
				for j in range(p1.SIZE):
					if p1.radar[i][j] in [p1.miss,p1.sink]:
						c+=1
			print "victory in %d moves" %(c)
			break
	except IndexError:
		print "yahan pahunche the"
		break
