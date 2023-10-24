from collections import defaultdict
from collections import Counter
import random
import argparse 
import os
import glob
from tkinter import *


values = {'2':1, '3':2, '4':3, '5':4, '6':5, '7':6,'8':7,'9':8,'10':9,'11':10, '12':11, '13': 12, '1':13}
suits = {'C': 1, 'D':2, 'H':3, 'S':4}
def getPlayers():
    theplayers = dict()
    for line in NewPlayer.lstofplayers:
        theplayers[line[0]] = line[1:]
    return theplayers

def highCard(hand):
    lstofcard = []
    for card in hand: #iterates through the 5 cards given to the player
        lstofcard.append(values[card[1:]]) 
    lstofcard = sorted(lstofcard, key=lambda x:-x) #sorts the cards from greatest to least greatest
    return (9, lstofcard[0], lstofcard[1])
        
def pairs(hand):
    highestPair = (0,0)
    lstofhigh = [] #stores the cards values
    for card in hand:
        lstofhigh.append(card[1:])
    d = sorted(lstofhigh, key = lstofhigh.count, reverse = True) #sorts the list by count
    if d.count(d[0]) == 2 and len(d) > 2:
        secondary = sorted(d[2:], key = lambda x: values[x], reverse =True)[0]
        highestPair = (values[d[0]], values[secondary])
    if highestPair == (0,0): #returns 0 if there are no pairs
        return (8, 0)
    return (8, int(highestPair[0]), int(highestPair[1]))

def twoPairs(hand):
    highestTwoPair = (0,0,0) #Used for comparison later in loop (needed for variable assignment references)
    lstofhigh = [] #This variable resets for each player (contains the list of cards each player has)
    for card in hand: #Iterates through each card
        lstofhigh.append(card[1:]) #Appends the value associated with each card (suit is discarded)
    # d = sorted(lstofhigh, key = lambda x: (x.count, values[x]), reverse = True) #sorts the list by count
    counter = Counter(lstofhigh)
    d = sorted(lstofhigh, key = lambda x: (counter[x], values[x]), reverse = True)
    if len(d) > 2 and d.count(d[0]) == 2 and d.count(d[2]) == 2:
        secondary = sorted(d[4:], key = lambda x: values[x], reverse = True)[0]
        if values[d[0]] > values[d[2]]:
            highestTwoPair = (values[d[0]], values[d[2]], values[secondary])
        elif values[d[2]] > values[d[0]]:
            highestTwoPair = (values[d[2]], values[d[0]], values[secondary])
    if highestTwoPair == (0,0,0): #if there were no double pairs returns a zero
        return (7, 0, 0, 0)
    return (7, int(highestTwoPair[0]), int(highestTwoPair[1]),  int(highestTwoPair[2])) #returns the player number that won

def threeOfAKind(hand):
    highestTriple = (0,0)
    lstofhigh = [] #stores the cards values
    for card in hand:
        lstofhigh.append(card[1:])
    d = sorted(lstofhigh, key = lstofhigh.count, reverse = True) #sorts the list by count
    if d.count(d[0]) == 3:
        secondary = sorted(d[3:], key = lambda x: values[x], reverse =True)[0]
        highestTriple = (values[d[0]], values[secondary])
    if highestTriple == (0,0): #returns 0 if there are no pairs
        return (6, 0)
    return (6, int(highestTriple[0]), int(highestTriple[1]))

def straight(hand):
    highestStraight = (0, 0)
    lstofhigh = set() #stores the cards values
    for card in hand:
        lstofhigh.add(values[card[1:]])
    count = 0
    lst = []
    for rank in reversed((1, *range(2,14))):
        if rank in lstofhigh:
            count +=1
            lst.append(rank)
            if count == 5:
                highestStraight = (5, lst[0])
        else:
            count = 0
            lst = []
    if highestStraight == (0,0):
        return (5,0)
    return highestStraight

def flush(hand):
    currentWinnerSuit = (0,0,0)
    lstofhigh = defaultdict(list) #stores the cards values
    for card in hand:
        lstofhigh[card[0]].append(values[card[1:]])
    for suit, vals in lstofhigh.items():
        if len(vals) == 5:
            currentWinnerSuit = (4, suits[suit], max(vals))
    if currentWinnerSuit == (0,0,0): #returns 0 if they are no flushes
        return (4,0,0)
    return currentWinnerSuit

def fullHouse(hand):
    fullHouse = (0,0,0) #stores the player num, the value of the triple, and the value of the double
    lstofhigh = []
    for card in hand:
        lstofhigh.append(card[1:])
    counter = Counter(lstofhigh) #creates a dictionary with the counts of each number
    if counter.most_common(2)[0][1] >= 3 and counter.most_common(2)[1][1] >= 2: #if the top 2 most frequent numbers appear 3 and 2 times then it returns true
        fullHouse = (3, values[counter.most_common(2)[0][0]], values[counter.most_common(2)[1][0]])
    if fullHouse == (0,0,0): #return 0 if there are no full houses
        fullHouse = (3, 0, 0)
    return fullHouse

def fourOfAKind(hand):
    quad = (0,0,0)
    lstofhigh = []
    for card in hand:
        lstofhigh.append(card[1:])
    d = sorted(lstofhigh, key = lstofhigh.count, reverse = True)
    if d.count(d[0]) == 4:
        secondary = sorted(d[4:], key = lambda x: values[x], reverse =True)[0]
        quad = (2, values[d[0]], values[secondary])
    if quad == (0,0,0):
        quad = (2,0,0)
    return quad

def straightFlush(hand):
    highestStraight = (0, 0, 0)
    lstofhigh = defaultdict(list) #stores the cards values
    for card in hand:
        lstofhigh[card[0]].append(int(card[1:]))
    for suit, vals in lstofhigh.items():
        if len(vals) >= 5:
            setvals = set(vals)
            setvals = sorted(setvals, reverse = True)
            count = 0
            lst = []
            for rank in reversed((1, *range(2,14))):
                if rank in setvals:
                    count +=1
                    lst.append(rank)
                    if count == 5:
                        highestStraight = (1, lst[0], suits[suit])
                else:
                    count = 0
                    lst = []
    if highestStraight == (0,0,0):
        highestStraight = (1,0,0)
    return highestStraight

def royalFlush(hand):
    highestStraight = (0, 0)
    lstofhigh = set() #stores the cards values
    for card in hand:
        lstofhigh.add(values[card[1:]])
    count = 0
    lst = []
    for rank in reversed((9, *range(10,14))):
        if rank in lstofhigh:
            count +=1
            lst.append(rank)
            if count == 5:
                highestStraight = (0, lst[0])
        else:
            count = 0
            lst = []
    if highestStraight == (0,0):
        return (0,0)
    return highestStraight

def fileHighCard(players):
    lstofhigh = []
    for player, cards in players.items(): #takes the keys and the values of the dictionary of players
        lstofcard = []
        for card in cards: #iterates through the 5 cards given to the player
            lstofcard.append(values[card[1:]]) 
        lstofcard = sorted(lstofcard, key=lambda x:-x) #sorts the cards from greatest to least greatest
        lstofhigh.append((player, lstofcard)) #appends the player and their list of cards (sorted)
    currentWin = lstofhigh[0] #sets the winner to the first player
    for player in lstofhigh[1:]: #for the player 2 and on
        if max(player[1]) == max(currentWin[1]): #if the current winner ties with the current player
            if max(player[1][1:]) > max(currentWin[1][1:]): #it checks what the highest value is other than the first highest
                currentWin = player
        elif max(player[1])> max(currentWin[1]): #changes it if they didn't tie
            currentWin = player
    return (1, int(currentWin[0]))
        
def filePairs(players):
    highestPair = (0,0,0)
    for player, cards in players.items(): #takes the keys and the values of the dictionary of players
        lstofhigh = [] #stores the cards values
        for card in cards:
            lstofhigh.append(card[1:])
        counter = Counter(lstofhigh) #creates a dictionary with the counts of each number
        for num, amount in counter.items(): #for the number and its frequency
            if amount == 2 and int(values[num]) > int(highestPair[1]): #if theres a pair and it has a higher value than the current value it will return true
                highestPair = (player, values[num], num)
    if highestPair == (0,0,0): #returns 0 if there are no pairs
        return (2, -1)
    return (2, int(highestPair[0]))

def fileTwoPairs(players):
    highestTwoPair = (0,0,0) #Used for comparison later in loop (needed for variable assignment references)
    for player, cards in players.items(): #takes the keys and the values of the dictionary of players
        lstofhigh = [] #This variable resets for each player (contains the list of cards each player has)
        for card in cards: #Iterates through each card
            lstofhigh.append(card[1:]) #Appends the value associated with each card (suit is discarded)
            lstofhigh = sorted(lstofhigh, key= lambda x: values[x]) #sorts the list using the dictionary of values stored above
        counter = Counter(lstofhigh) #creates a counter dictionary tracking how many times a certain value appears in each players hand
        count = 0 #counter variable to track if a pair comes up twice
        lstofPairs = [] #empty list to add the value of the pairs (needed for tie breaker)
        for num, amount in counter.items(): #iterates through the value and the amount of time it appears in the counter dictionary
            if amount == 2: # 'if there are two pairs'
                lstofPairs.append(int(num)) #append the value of the pair
                lstofPairs.sort() #sort the list so I can keep track of the smaller valued pair
                count += 1 #increase the count for the counter
                if count ==2 and int(values[num]) > int(highestTwoPair[1]): #will replace the original variable if true and replace any higher paired number
                    highestTwoPair = (player, values[num], num)
                    secondPair = lstofPairs[0]
                elif count ==2 and int(values[num]) ==int(highestTwoPair[1]): #if the highest numbers tie then it will check the second pair of values
                    if secondPair < lstofPairs[0]:
                        highestTwoPair = (player, values[num], num)
                        secondPair = lstofPairs[0]
    if highestTwoPair == (0,0,0): #if there were no double pairs returns a zero
        return (3, -1)
    return (3, int(highestTwoPair[0])) #returns the player number that won

def fileThreeOfAKind(players):
    highestPair = (0,0,0) #stores the player num, the value of triple value, and the highest value past the triple
    for player, cards in players.items(): #takes the keys and the values of the dictionary of players
        lstofhigh = [] #stores the cards values
        for card in cards:
            lstofhigh.append(card[1:])
        counter = Counter(lstofhigh) #creates a dictionary with the counts of each number
        sortLst = sorted(lstofhigh, key = lstofhigh.count, reverse = True) #sorts the list by count
        for num, amount in counter.items(): #for the number and the frequency
            if amount == 3 and int(values[num]) == int(highestPair[1]): #if there is a triple and the values tie it goes to the highest value past the triple
                if max(sortLst) > int(highestPair[2]): 
                    highestPair = (player, values[num], max(sortLst))
            elif amount == 3 and int(values[num]) > int(highestPair[1]): #if there is a triple and the value of the current number is greater it rebinds the variable
                sortLst = sorted(sortLst[3:], key= lambda x: values[x], reverse = True)
                highestPair = (player, values[num], values[sortLst[0]])
    if highestPair == (0,0,0): #returns 0 if there is no triple
        return (4, -1)
    return (4, int(highestPair[0]))

def fileStraight(players):
    highestStraight = (0, 0)
    for player, cards in players.items(): #takes the keys and the values of the dictionary of players
        lstofhigh = [] #stores the cards values
        for card in cards:
            lstofhigh.append(values[card[1:]])
        if sorted(lstofhigh) == list(range(min(lstofhigh), max(lstofhigh) +1)) and max(lstofhigh) > highestStraight[1]: #if the cards are in a straight
            highestStraight = (player, max(lstofhigh)) #binds the players num and the highest value of the straight
    if highestStraight == (0, 0): #if there is no straight it will return 0
        return (5, -1)
    return (5, int(highestStraight[0]))

def fileFlush(players):
    currentWinnerSuit = (0, 0)
    for player, cards in players.items(): #takes the keys and the values of the dictionary of players
        lstofhigh = [] #stores the cards values
        for card in cards:
            lstofhigh.append(card[0])
        if all(x == lstofhigh[0] for x in lstofhigh) and suits[lstofhigh[0]] > currentWinnerSuit[1]: #if all the suits in the list are the same and the suit is greater than the current winner
            currentWinnerSuit = (player, suits[lstofhigh[0]]) #stores the player num and the value of the suits
    if currentWinnerSuit == (0,0): #returns 0 if they are no flushes
        return (6,-1)
    return (6, int(currentWinnerSuit[0]))

def fileFullHouse(players):
    highestPair = (0,0,0) #stores the player num, the value of the triple, and the value of the double
    for player, cards in players.items(): #takes the keys and the values of the dictionary of players
        lstofhigh = []
        for card in cards:
            lstofhigh.append(card[1:])
        counter = Counter(lstofhigh) #creates a dictionary with the counts of each number
        if counter.most_common(2)[0][1] == 3 and counter.most_common(2)[1][1] == 2: #if the top 2 most frequent numbers appear 3 and 2 times then it returns true
            if values[counter.most_common(2)[0][0]] == highestPair[1]: #if the triple's value is equal to the current highest triple
                if values[counter.most_common(2)[1][0]] > highestPair[2]: #if the pairs value is greater than the current highest's double
                    highestPair = (player, values[counter.most_common(2)[0][0]],  values[counter.most_common(2)[1][0]])
            elif values[counter.most_common(2)[0][0]] > highestPair[1]: #if the triple's value is greater than the current highest triple
                highestPair = (player, values[counter.most_common(2)[0][0]],  values[counter.most_common(2)[1][0]])
    if highestPair == (0,0,0): #return 0 if there are no full houses
        return (7, -1)
    return (7, int(highestPair[0]))

def fileFourOfAKind(players):
    highestPair = (0,0,0)
    for player, cards in players.items(): #takes the keys and the values of the dictionary of players
        lstofhigh = []
        for card in cards:
            lstofhigh.append(card[1:])
        counter = Counter(lstofhigh) #creates a dictionary with the counts of each number
        for num, amount in counter.items():
            if amount == 4 and int(values[num]) == int(highestPair[1]): #if the frequency is 4 and the number ties with the curent highest
                if values[counter.most_common(2)[1][0]] > highestPair[2]: #if the 2nd highest valued number is larger the the 2nd highest value of the current highest
                    highestPair = (player, values[num], values[counter.most_common(2)[1][0]])
            elif amount == 4 and int(values[num]) > int(highestPair[1]): #if the value is greater than the current highest
                highestPair = (player, values[num], values[counter.most_common(2)[1][0]])
    if highestPair == (0,0,0): #return 0 if there are no 4 of a kind's
        return (8, -1)
    return (8, int(highestPair[0]))

def fileStraightFlush(players):
    highestStraight = (0, 0, 0) #stores the player number, the highest number of the straight, and the values associated with the suits dictionary
    for player, cards in players.items(): #takes the keys and the values of the dictionary of players
        lstofhigh = [] #stores the card values
        lstofsuits = [] #stores the suits
        for card in cards:
            lstofhigh.append(values[card[1:]])
            lstofsuits.append(card[0])
        if sorted(lstofhigh) == list(range(min(lstofhigh), max(lstofhigh) +1)) and all(x == lstofsuits[0] for x in lstofsuits): #if its a straight and all the suits are the same
            if max(lstofhigh) > highestStraight[1]: #if the largest number of the straight is higher than the current winner's largest number
                highestStraight = (player, max(lstofhigh), suits[lstofsuits[0]])
            elif max(lstofhigh) == highestStraight[1]: #if the numbers are equal
                if suits[lstofsuits[0]] > highestStraight[2]: #check if the suits higher than the current highest's
                    highestStraight = (player, max(lstofhigh), suits[lstofsuits[0]])
    if highestStraight == (0, 0, 0): #return 0 if there is no straight flush
        return (9, -1)
    return (9, int(highestStraight[0]))

def fileRoyalFlush(players):
    highestStraight = (0, 0) #Tracks the player and the value associated with the suit
    for player, cards in players.items(): #takes the keys and the values of the dictionary of players
        lstofhigh = [] #Stores the value of the cards
        lstofsuits = [] #Stores the suit
        for card in cards:
            lstofhigh.append(values[card[1:]])
            lstofsuits.append(card[0])
        if sorted(lstofhigh) == list(range(9, 14)) and all(x == lstofsuits[0] for x in lstofsuits): #if its a straight starting from 10 (valued at 9 according to the value dictionary) and all the suits are the same
            if suits[lstofsuits[0]] > highestStraight[1]: #if the suit is larger than the current winner's suit
                highestStraight = (player, suits[lstofsuits[0]])
    if highestStraight == (0, 0): #if none of the players have a royal flush return 0
        return (10, -1)
    return (10, int(highestStraight[0]))

def get_winner(filepath): #returns a string that denotes the winner
    hand = dict()
    for line in open(filepath):
        split = line.rstrip('\n').split(',')
        hand[split[0]] = split[1:]
    comboList = [] #Used to store the values returned by all the functions
    for combo in fileHighCard(hand), filePairs(hand), fileTwoPairs(hand), fileThreeOfAKind(hand), fileStraight(hand), fileFlush(hand), fileFullHouse(hand), fileFourOfAKind(hand), fileStraightFlush(hand), fileRoyalFlush(hand):
        comboList.append(combo)
    comboList = sorted(comboList, key = lambda x: x[0], reverse = True) #Sort the list from largest to smallest (largest being the highest ranked aka. royal flush and smallest being lower ranked aka. highcard)
    for combo in comboList:
        if combo[1] != -1: #If the value associated is 0 that means it did not meet the requirements of the combo and goes to the next combo
            return str(combo[1])

def findWinner(hand): #returns a string that denotes the winner
    comboList = [] #Used to store the values returned by all the functions
    for combo in highCard(hand), pairs(hand), twoPairs(hand), threeOfAKind(hand), straight(hand), flush(hand), fullHouse(hand), fourOfAKind(hand), straightFlush(hand), royalFlush(hand):
        comboList.append(combo)
    comboList = sorted(comboList, key = lambda x: -x[0], reverse = True) #Sort the list from largest to smallest (largest being the highest ranked aka. royal flush and smallest being lower ranked aka. highcard)
    for combo in comboList:
        if combo[1] != 0: #If the value associated is 0 that means it did not meet the requirements of the combo and goes to the next combo
            return combo

class NewPlayer:
    numofplayers = 0
    lstofplayers = []
    def __init__(self, money = 10):
        NewPlayer.numofplayers = NewPlayer.numofplayers + 1
        self.playername = 'Player ' + str(NewPlayer.numofplayers)
        self.cards = [self.playername]
        self.cards.extend(Game.deck[:2])
        self.deck = []
        self.deck.extend(Game.deck[:2])
        self.cards.extend(Game.communitycards)
        del Game.deck[:2]
        NewPlayer.lstofplayers.append(self.cards)
        self.money = money
    
    def resetPlayers(self):
        self.cards = [self.playername]
        self.cards.extend(Game.deck[:2])
        self.deck = []
        self.deck.extend(Game.deck[:2])
        self.cards.extend(Game.communitycards)
        del Game.deck[:2]
        NewPlayer.lstofplayers.append(self.cards)

class Game:
    deck = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13','D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13','C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13']
    random.shuffle(deck)
    communitycards = []
    communitycards.extend(deck[:3])
    del deck[:3]
    def __init__(self, n_player):
        self.n_player = n_player
        self.moneypool = 0
    def resetGame(self):
        Game.deck = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13','D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13','C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13']
        random.shuffle(Game.deck)
        Game.communitycards = []
        Game.communitycards.extend(Game.deck[:3])
        del Game.deck[:3]

class GUI():

    def __init__(self, n_players):
        self.root = Tk()
        self.root.title('Texas Hold \'Em')
        self.root.geometry('400x400')
        self.root.resizable(1,1)
        self.n_players= n_players + 1
        self.Start = Game(n_players)    
        self.AllPlayers = [NewPlayer() for i in list(range(1,self.Start.n_player + 1))]
        self.Start.moneypool = 10
        self.round1Complete = False
        self.round2Complete = False
        self.gameInitialization()
    
    def gameInitialization(self):
        InitGame = Label(self.root, text = '~~~~~~~Initialization Game~~~~~~~')
        InitGame.pack()
        YourHand = Label(self.root, text = 'Your Hand: ' + str(self.AllPlayers[0].deck))
        YourHand.pack()
        self.players = getPlayers()
        print(self.players)
        print(Game.communitycards)
        self.allHands = []
        for player, hand in self.players.items():
            y = findWinner(hand[:2])
            self.allHands.append((y, player))
        self.folds = self.botMove()
        if all(self.folds) == True:
            self.folded = False
        else:
            question = Label(self.root, text = 'Do you want to Bet or Fold: ')
            question.pack()
            self.answer = StringVar()
            betAction = Entry(self.root, textvariable = self.answer, bg='White')
            betAction.insert(END, 'Type Action Here!')
            betAction.pack()
            submitAction = Button(self.root, text = 'Confirm Action', command = lambda: self.betFoldOrError(self.answer))
            submitAction.pack()
  
    def resetGUI(self):
        for child in self.root.winfo_children():
            child.destroy()
    
    def restartGame(self):
        self.Start.resetGame()
        for player in self.AllPlayers:
            player.resetPlayers()
        self.resetGUI()
        self.round1Complete = False
        self.round2Complete = False
        self.gameInitialization()

    def runUI(self):
        self.root.mainloop()
    
    def botMove(self):
        botsFolded = []
        for player in self.AllPlayers[1:]:
            for hand in self.allHands:
                if player.playername == hand[1]:
                    player.rank = hand[0]
            if int(player.rank[0]) == 9:
                player.money -= 1
                self.Start.moneypool += 1
                botBetLabel = Label(self.root, text = player.playername + ' bets $1')
                botBetLabel.pack()
                botsFolded.append(False)
            elif int(player.rank[0]) < 9 and int(player.rank[0]) >= 5:
                player.money -= 2
                self.Start.moneypool += 2
                botBetLabel = Label(self.root, text = player.playername + ' bets $2')
                botBetLabel.pack()
                botsFolded.append(False)
            elif int(player.rank[0]) < 5 and int(player.rank[0]) >= 2:
                player.money  -= 3
                self.Start.moneypool += 3
                botBetLabel = Label(self.root, text = player.playername + ' bets $3')
                botBetLabel.pack()
                botsFolded.append(False)
            elif int(player.rank[0]) == 1:
                player.money  -= 5
                self.Start.moneypool += 5
                botBetLabel = Label(self.root, text = player.playername + ' bets $5')
                botBetLabel.pack()
                botsFolded.append(False)
            else:
                botBetLabel = Label(self.root, text = player.playername + 'folds')
                botBetLabel.pack()
                botsFolded.append(True)
        return botsFolded
    
    def checkWin(self):
        self.resetGUI()
        if all(self.folds) == True:
            winLabel = Label(self.root, text = 'Winner: Player 1')
            winLabel.pack()
            self.AllPlayers[0].money = self.AllPlayers[0].money + self.Start.moneypool
            self.Start.moneypool = 0
        elif self.folded == False:
            winner = 0
            for hands in self.allHands:
                if winner == 0:
                    winner = hands
                elif hands[0][0] < winner[0][0]:
                    winner = hands
                elif hands[0][0]== winner[0][0]:
                    if hands[0][1] > winner[0][1]:
                        winner = hands
            winLabel = Label(self.root, text = 'Winner: ' + winner[1])
            winLabel.pack()
            for player in self.AllPlayers:
                if player.playername == winner[1]:
                    player.money = player.money + self.Start.moneypool
                    self.Start.moneypool = 0
        elif self.folded == True:
            winner = 0
            for hands in self.allHands[1:]:
                if winner == 0:
                    winner = hands
                elif hands[0][0] < winner[0][0]:
                    winner = hands
                elif hands[0][0]== winner[0][0]:
                    if hands[0][1] > winner[0][1]:
                        winner = hands
            winLabel = Label(self.root, text = 'Winner: ' + winner[1])
            winLabel.pack()
        for playernum in range(len(self.AllPlayers) + 1):
            for player in self.AllPlayers:
                if player.playername == 'Player ' + str(playernum):
                    player = Label(self.root, text = player.playername + ': $' + str(player.money))
                    player.pack()
        for player in self.AllPlayers:    
            if player.money <= 0:
                for person in NewPlayer.lstofplayers:
                    if player.playername == person[0]:
                        NewPlayer.lstofplayers.remove(person)
                self.AllPlayers.remove(player)
                self.Start.n_player = self.Start.n_player - 1
        if self.round1Complete == False:
            self.round1()
        elif self.round2Complete == False:
            self.round2()
        elif self.round1Complete == True and self.round2Complete == True:
            finishedLabel = Label(self.root, text = 'The game is now done.')
            finishedLabel.pack()
            restartButton = Button(self.root, text = 'Restart Game', command = self.restartGame)
            restartButton.pack()
            quitButton = Button(self.root, text = 'Quit Game', command = self.root.destroy)
            quitButton.pack()

    def calcVal(self, bettingValVar):
        if int(bettingValVar.get()) > self.AllPlayers[0].money or int(bettingValVar.get()) < 1:
            valueErrorLabel = Label(self.root, text = 'Invalid Value was entered.')
            valueErrorLabel.pack()
        else:
            self.AllPlayers[0].money -= int(bettingValVar.get())
            self.Start.moneypool += int(bettingValVar.get())
            self.checkWin()
    
    def round1(self):
        self.round1Complete = True
        round1Label = Label(self.root, text = '~~~~~~~~~~ Round 1 ~~~~~~~~~~')
        round1Label.pack()
        YourHand = Label(self.root, text = 'Your Hand: ' + str(self.AllPlayers[0].deck))
        YourHand.pack()
        communityCardLabel = Label(self.root, text = 'Community Cards' + str(Game.communitycards))
        communityCardLabel.pack()
        self.allHands = []
        for player, hand in self.players.items():
            y = findWinner(hand)
            self.allHands.append((y, player))
        self.folds = self.botMove()
        if all(self.folds) == True:
            self.folded = False
        else:
            question = Label(self.root, text = 'Do you want to Bet or Fold: ')
            question.pack()
            self.answer = StringVar()
            betAction = Entry(self.root, textvariable = self.answer, bg='White')
            betAction.insert(END, 'Type Action Here!')
            betAction.pack()
            submitAction = Button(self.root, text = 'Confirm Action', command = lambda: self.betFoldOrError(self.answer))
            submitAction.pack()
    
    def round2(self):
        self.round2Complete = True
        YourHand = Label(self.root, text = 'Your Hand: ' + str(self.AllPlayers[0].deck))
        YourHand.pack()
        round2Label = Label(self.root, text = '~~~~~~~~~~ Round 2 ~~~~~~~~~~')
        round2Label.pack()
        Game.communitycards.extend(Game.deck[:2])
        for player in self.players.keys():
            self.players[player].extend(Game.deck[:2])
        del Game.deck[:2]       
        communityCardLabel = Label(self.root, text = 'Community Cards' + str(Game.communitycards))
        communityCardLabel.pack()
        self.allHands = []
        for player, hand in self.players.items():
            y = findWinner(hand)
            self.allHands.append((y, player))
        self.folds = self.botMove()
        if all(self.folds) == True:
            self.folded = False
        else:
            question = Label(self.root, text = 'Do you want to Bet or Fold: ')
            question.pack()
            self.answer = StringVar()
            betAction = Entry(self.root, textvariable = self.answer, bg='White')
            betAction.insert(END, 'Type Action Here!')
            betAction.pack()
            submitAction = Button(self.root, text = 'Confirm Action', command = lambda: self.betFoldOrError(self.answer))
            submitAction.pack()

    def betFoldOrError(self, answer):
        try:
            if answer.get() == 'Bet' or answer.get() == 'bet':
                self.folded = False
                self.resetGUI()
                bettingValLabel = Label(self.root, text = 'How much do you want to bet?: ')
                bettingValLabel.pack()
                bettingValVar = IntVar()
                bettingValEntry = Entry(self.root, textvariable = bettingValVar)
                bettingValEntry.pack()
                submitVal = Button(self.root, text = 'Submit Value', command = lambda: self.calcVal(bettingValVar))
                submitVal.pack()
            elif answer.get() == 'Fold' or answer.get() == 'fold':
                self.resetGUI()
                foldLabel = Label(self.root, text = 'Player has folded')
                foldLabel.pack()
                self.folded = True
                self.checkWin()
            else:
                raise NameError
        except NameError:
            Invalid = Label(self.root, text = 'Invalid Command, Respond with \'bet\' or \'fold\'. Try Again')
            Invalid.pack()
        except ValueError:
            Invalid = Label(self.root, text = 'Invalid Command. Try Again')
            Invalid.pack()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--usermode', action= 'store_true')
    parser.add_argument('-f', '--filemode', action= 'store_true')
    parser.add_argument('-p', '--players', type= int)
    parser.add_argument('-i', '--index', type = str)
    args = parser.parse_args()
    if args.usermode and args.players is None:
        parser.error('You need to specify the number of players in User Mode')
    if args.filemode and args.index is None:
        parser.error('You need to specify the filepath in File Mode')
    if args.filemode:
        os.chdir(args.index)
        for file in glob.glob('*.txt'):
            print(file, get_winner(file))
    if args.usermode:
        myGUI = GUI(args.players)
        myGUI.runUI()


if __name__ == '__main__':
    main()

