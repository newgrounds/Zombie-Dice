import random

class Main:
	def __init__(self):
		self.players = [Player(True),
						Player(),
						Player(),
						Player()] #list
		self.dice = [GreenDice(),
					GreenDice(),
					GreenDice(),
					GreenDice(),
					GreenDice(),
					GreenDice(),
					YellowDice(),
					YellowDice(),
					YellowDice(),
					YellowDice(),
					RedDice(),
					RedDice(),
					RedDice()] #list
		
	# prints each player's stats after the game ends
	def endGame(self):
		for p in self.players:
			print "The Final Results:"
			print "Player", self.players.index(p)+1, "had", p.brains, "brains."
		
		r = raw_input("Would you like to play again?")
		if r=="yes" or r=="y" or r=="Yes" or r=="Y":
			Main().turn()
		else:
			print "Game Over! Thanks for playing.\n"
			
	# switches to the next player's turn
	def nextTurn(self):
		if self.anybodyWin() & self.sameNumTurns():
			self.endGame()
		else:
			for p in self.players:
				if p.turn == True:
					plyr = p
			plyrNum = self.players.index(plyr)
			plyr.turn = False
			if plyrNum+1 == len(self.players):
				self.players[0].turn = True
			else:
				self.players[plyrNum+1].turn = True
			self.turn()
	
	# appends everything in y onto x
	def appendList(self, x, y):
		for i in y:
			x.append(i)
		return x
	
	# checks that all players got the same number of turns
	def sameNumTurns(self):
		totalTurns = self.players[0].turns #int
		same = False #Boolean
		for p in self.players:
			same = (totalTurns == p.turns)
		return same
	
	# determines if anyone has reached 13 brains
	def anybodyWin(self):
		win = False #Boolean
		for p in self.players:
			if p.won():
				win = True
		return win
	
	# picks dice for the next roll while reusing all "footprint" dice		
	def dicePicker(self, footprints):
		unrolled = [] #list
		rolled = [] #list
		pickedDice = [] #list of dice to be rolled
		
		# add footprints to list
		pickedDice = self.appendList(pickedDice, footprints)
		
		# populate the lists of rolled and unrolled
		for d in self.dice:
			if d.rolled:
				rolled.append(d)
				for i in footprints:
					if i == d:
						rolled.remove(i)
			else:
				unrolled.append(d)
			
		if len(unrolled) + len(footprints) >= 3:
			pickedDice = self.appendList(pickedDice, 
									random.sample(unrolled, 3-len(pickedDice)))
		else:
			pickedDice = self.appendList(pickedDice, unrolled)
			pickedDice = self.appendList(pickedDice, 
									random.sample(rolled, 
												3-len(pickedDice)))
			for j in self.dice:
				for k in pickedDice:
					if j != k:
						j.rolled = False
		return pickedDice
	
	# handles the main action of the game, player turns
	def turn(self):
		for p in self.players:
			if p.turn == True:
				plyr = p #int
				if self.anybodyWin():
					print "Player " + str(self.players.index(p)+1) + "'s Last Turn"
				else:
					print "Player " + str(self.players.index(p)+1) + "'s Turn"
		cont = True #Boolean to keep loop going for each turn
		reuseDice = [] #list of dice that rolled footprints
		b = 0 #int to hold number of brains rolled
		s = 0 #int to hold number of shotguns rolled
		while cont:
			raw_input("Press Enter to Roll:") #string
			
			pickedDice = self.dicePicker(reuseDice) #list of dice to roll
			reuseDice = []
			
			for i in pickedDice:
				g = i.roll() #string
				if g == "shotgun":
					s += 1
					print "Shotgun!"
				elif g == "brain":
					b += 1
					print "Brain!"
				elif g == "footprint":
					reuseDice.append(i)
					print "Footprint!"
			
			print "Total Brains:", plyr.brains + b, " Total Shotguns:", s, " Footprints:", len(reuseDice)
			
			if s >= 3:
				print "You have", s, "shotguns, so you are dead!"
				print "Your total number of brains is back at", plyr.brains, "\n"
				plyr.turns += 1
				cont = False
				self.nextTurn()
					
			else:	
				r = raw_input("End Turn?")
				if r=="yes" or r=="y" or r=="Yes" or r=="Y":
					plyr.brains += b
					print "Your total number of brains is", plyr.brains, "\n"
					plyr.turns += 1
					cont = False
					self.nextTurn()
				else:
					print

class Player:
	def __init__(self, t=False):
		self.turn = t #Boolean
		self.brains = 0 #int
		self.turns = 0 #int
	
	def won(self):
		return self.brains >= 13

class Dice:
	sides = [] #list
	color = "Green" #string
	rolled = False #Boolean
	
	def __init__(self):
		pass
	
	def roll(self):
		pickedSide = random.choice(self.sides) #string
		self.rolled = True
		return pickedSide

class GreenDice(Dice):
	def __init__(self):
		self.sides = ["footprint",
					"footprint",
					"brain",
					"brain",
					"brain",
					"shotgun"] #list
		self.color = "Green"

class YellowDice(Dice):
	def __init__(self):
		self.sides = ["footprint",
					"footprint",
					"brain",
					"brain",
					"shotgun",
					"shotgun"] #list
		self.color = "Yellow"	

class RedDice(Dice):
	def __init__(self):
		self.sides = ["footprint",
					"footprint",
					"brain",
					"shotgun",
					"shotgun",
					"shotgun"] #list
		self.color = "Red"

m = Main()
m.turn()

print GreenDice().sides
print YellowDice().sides
print RedDice().sides
print m.dice
print m.players
print "First Player's Brains:", m.players[0].brains
print m.dice[4].rolled