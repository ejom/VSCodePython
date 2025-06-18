import random

suits = ["Hearts", "Clubs", "Diamonds", "Spades"]
ranks = list(range(1, 14))

class Cards:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append((rank, suit))
    def draw(self):
        card = self.deck[0]
        self.deck.remove(card)
        return card
    def shuffle(self):
        random.shuffle(self.deck)

class Player:
    def __init__(self, name, money):
        if isinstance(name, str) and name != "":
            self.name = name
        else:
            raise TypeError("Player name must be a string")
        if isinstance(money, int) and money>0: 
            self.money = money
        else:
            raise TypeError("money must be an integer")
    def __str__(self):
        return f"{self.name} has {self.money} left."
    def bet(self, amount):
        if self.money >= amount:
            self.money -= amount
            return amount
        else:
            print(f"{self.name} doesn't have {amount}. Would you like to go all in and bet {self.money}?")
            allIn = input("Type y or yes if you are going all in or anything else if not.")
            if allIn[0].lower() == 'y':
                print("You are all in.")
                amount = self.money
                self.money = 0
                return (amount, True)
            else: 
                print("You bet nothing.")
                return 0


def makePlayers(numPlayers, startMoney=0):
    players = list(range(numPlayers))
    for i in range(numPlayers):
        while True:
            try:
                name = input(f"Enter the name for player {i+1}: ")
                money = startMoney if startMoney else int(input("Enter your starting cash: "))
                break
            except:
                print("Invalid input. Try again.")
        players[i] = Player(name, money)
    print("Players recap:")
    print(*players)
    return players

def round(players):
    roundPot=0
    currentBet=0
    playerBets = [0] * len(players)
    playersIn = [1] * len(players)

    while True:
        for i, player in enumerate(players):
            #IMPLEMENT?
            #Right now if the previous player folded the next player has an 
            # oppertunity to bet even if all the bets are the same (as those conditions are skipped).
            #Maybe make it not so?

            #If you folded you dont get a turn
            if not playersIn[i]:
                continue
            #Update the pot with everyone's bets
            roundPot = sum(playerBets)
            #Reset this in case the last player folded
            didFold = False

            print()
            print("-"*20+f"{players[i].name}'s turn"+"-"*20)
            print(player)
            #Recap the currentBet and player's bet
            print(f"Your bet so far is ${playerBets[i]}. The current bet on the pot is ${currentBet}")
            #Determine if the player can bet/check or if they need to match/raise/fold
            #bet/check
            if playerBets[i] == currentBet:
                print("You can bet (enter a number>0) or check (enter 0)?")
                while True:
                    try:
                        playerBets[i] += int(input("Enter how much to raise the current bet (int): "))
                        break
                    except:
                        print("Invalid input. Try again.")
                currentBet = playerBets[i]
            #match/raise/fold
            else:
                print("Would you like to raise/match the current bet or fold?")
                print(f"To meet the current bet you must enter at least {currentBet-playerBets[i]}")
                while True:
                    try:
                        choice = input("Enter f for fold or enter the amount of your bet for raise/match: ")
                        #Make sure they are betting an int
                        x = int(choice)
                        #Make sure they bet the minimum to match
                        if x < currentBet-playerBets[i]:
                            print("Bet is lower than the minimum bet")
                            raise Exception("Bet is lower than the minimum bet")
                        break
                    except:
                        #If its not a number than the player's input is either folding or invalid
                        #Folding
                        if choice[0].lower() == 'f':
                            print("You folded")
                            #DO: implement pulling playerBet from player's money 
                            playersIn[i] = 0
                            #See if there's only one player left
                            if sum(playersIn) == 1:
                                print("We have a winner")
                                return roundPot
                            #Use this so we skip rest of for loop
                            didFold = True
                            break
                        #Invalid, stuck in while loop until valid input is given (f or big enough number)
                        print(f"This is either an invalid input or below {currentBet-playerBets[i]}. Try again")
                #Get out of the for loop immediately if the player folded and move to next player
                if didFold:
                    continue
                #Once we determine that the raise is valid add it to their current bet. 
                playerBets[i] += x
                #Update current bet (if might be unecessary)
                if playerBets[i] > currentBet:
                    currentBet = playerBets[i]

            #build an array of everyone's current bet that is still in
            playerBetsIn = []
            for i, isIn in enumerate(playersIn):
                if isIn:
                    playerBetsIn.append(playerBets[i])
            #As long as its not the first turn (all zeros), we end the round if everyone's bet is the same
            if all(x==currentBet and not x==0 for x in playerBetsIn):
                return roundPot
        #If everyone's bet is the same by the last turn (they all checked) end the round
        if all(x==currentBet for x in playerBetsIn):
            return roundPot

print(round(makePlayers(3, 100)))

