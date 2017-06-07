import battleship

battleship.boardgenerator()
c=0
while True:
	try:
		x,y = battleship.nextmove()
		battleship.hitat(x,y)
		if battleship.radar[x][y]==battleship.hit:
			battleship.target_mode(x,y)
		if len(battleship.ships)==0:
			for i in range(battleship.SIZE):
				for j in range(battleship.SIZE):
					if battleship.radar[i][j] in [battleship.miss,battleship.sink]:
						c+=1
			print "victory in %d moves" %(c)
			break
	except IndexError:
		print "yahan pahunche the"
		break
