import random
import direct.directbase.DirectStart
import direct.gui.OnscreenText
from direct.gui.DirectGui import *
from pandac.PandaModules import *

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
        infoText['text'] = "The Final Results:\n"
        for p in self.players:
            infoText['text'] += "Player " + str(self.players.index(p)+1) + " had " + str(p.brains) + " brains.\n"
        
        endB['state'] = DGG.DISABLED
        rollB['state'] = DGG.DISABLED
        
        startB['scale'] = 0.15
        startB.setPos(0.0,0.0,-0.6)
        startB.show()
            
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
    
    def endTurn(self, plyr, b):
        plyr.brains += b
        infoText['text'] =  "Your total number of brains is " + str(plyr.brains) + "\n"
        plyr.turns += 1
        self.nextTurn()
    
    def roller(self, plyr, s, b, reuseDice):
        rollB['state'] = DGG.DISABLED
        endB['state'] = DGG.DISABLED
        
        pickedDice = self.dicePicker(reuseDice) #list of dice to roll
        
        infoText['text'] = "Current Roll:\n"
        
        for i in pickedDice:
            g = i.roll() #string
            if g == "shotgun":
                s += 1
                infoText['text'] += "Shotgun!\n"
            elif g == "brain":
                b += 1
                infoText['text'] += "Brain!\n"
            elif g == "footprint":
                reuseDice.append(i)
                infoText['text'] += "Footprint!\n"
                
        infoText['text'] += "Total Brains: " + str(plyr.brains + b) + "  Total Shotguns: " + str(s) + "  Footprints: " + str(len(reuseDice)) + "\n"
            
        if s >= 3:
            infoText['text'] += "\nYou have " + str(s) + " shotguns, so you are dead!\n"
            infoText['text'] += "Your total number of brains is back at " + str(plyr.brains) + "\n"
            infoText['text'] += "Press End Turn"
        else:
            endB['extraArgs'] = [plyr, b]
            rollB['command'] = self.roller
            rollB['extraArgs'] = [plyr, s, b, []]
            rollB['state'] = DGG.NORMAL
        
        endB['state'] = DGG.NORMAL
    
    # handles the main action of the game, player turns
    def turn(self):
        for p in self.players:
            if p.turn == True:
                plyr = p #int
                if self.anybodyWin():
                    turnText['text'] = "Player " + str(self.players.index(p)+1) + "'s Last Turn"
                else:
                    turnText['text'] = "Player " + str(self.players.index(p)+1) + "'s Turn"
        reuseDice = [] #list of dice that rolled footprints
        b = 0 #int to hold number of brains rolled
        s = 0 #int to hold number of shotguns rolled
        
        # handle buttons
        infoText['text'] = "Roll or End Turn\n"
        rollB['command'] = self.roller
        rollB['extraArgs'] = [plyr, s, b, reuseDice]
        rollB['state'] = DGG.NORMAL
        
        endB['command'] = self.endTurn
        endB['extraArgs'] = [plyr, b]
        endB['state'] = DGG.NORMAL
        
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

titleText = "Zombie Dice"
textText = OnscreenText(text = titleText, pos = (0.0,0.8,0.0), 
                        scale = 0.1,fg=(1,1,1,1),align=TextNode.ACenter)

rollB = DirectButton(text = ("Roll"), scale = .1, state = DGG.DISABLED)
rollB.setPos(-0.8,0.0,-0.8)

turnText = OnscreenText(text = "Player 1's Turn", pos = (0.0,0.5,0.0),
                        scale = 0.1,fg=(1,1,1,1),align=TextNode.ACenter,
                        mayChange = 1)

infoText = OnscreenText(text = "Click Below to Start the Game", pos = (0.0,0.3,0.0),
                        scale = 0.1,fg=(1,1,1,1),align=TextNode.ACenter,
                        mayChange = 1)

endB = DirectButton(text = ("End Turn"), scale = .1, state = DGG.DISABLED)
endB.setPos(0.8,0.0,-0.8)

def startGame():
    startB.hide()
    Main().turn()

startB = DirectButton(text = ("Start Game"), scale = .1, command=startGame)
startB.setPos(0.0,0.0,0.0)

run()