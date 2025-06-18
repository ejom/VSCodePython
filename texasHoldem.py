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
        self.allIn = False
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
                self.allIn=True
                return amount
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
    currentBet=0
    playerBets = [0] * len(players)
    playersIn = [1] * len(players)

    #Make sure all-in is reset
    for player in players:
        player.allIn = False

    while True:
        for i, player in enumerate(players):
            #IMPLEMENT?
            #Right now if the previous player folded the next player has an 
            # oppertunity to bet even if all the bets are the same (as those conditions are skipped).
            #Maybe make it not so?

            #If you arent in (folded or all in) you dont get a turn
            if not playersIn[i]:
                continue
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
                        x = int(input("Enter how much to raise the current bet (int): "))
                        break
                    except:
                        print("Invalid input. Try again.")
                playerBets[i] += player.bet(x)
                currentBet = playerBets[i]
            #match/raise/fold
            else:
                print("Would you like to raise/match the current bet or fold?")
                print(f"To meet the current bet you must enter at least {currentBet-playerBets[i]}. If you are going all in just enter the minimum bet")
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
                            playersIn[i] = 0
                            #See if there's only one player left
                            if sum(playersIn) <= 1:
                                print("We can determine a winner")
                                #IMPLEMENT: this should break through an outer game loop
                                return sum(playerBets)
                            #Use this so we skip rest of for loop
                            didFold = True
                            break
                        #Invalid, stuck in while loop until valid input is given (f or big enough number)
                        print(f"This is either an invalid input or below {currentBet-playerBets[i]}. Try again")
                playerBets[i] += player.bet(x)
                #if the player is all-in is similar process to folding.
                if player.allIn:
                    playersIn[i] = 0
                    #See if there's only one player left
                    if sum(playersIn) == 1:
                        print("We can determine a winner")
                        #IMPLEMENT: this should break through an outer game loop
                        return sum(playerBets)
                    continue
                #Get out of the for loop immediately if the player folded and move to next player
                if didFold:
                    continue
                #Once we determine that the raise is valid add it to their current bet. 
                currentBet = playerBets[i]

            print(*players)
            #build an array of everyone's current bet that is still in
            playerBetsIn = []
            for i, isIn in enumerate(playersIn):
                if isIn:
                    playerBetsIn.append(playerBets[i])
            #As long as its not the first turn (all zeros), we end the round if everyone's bet is the same
            if all(x==currentBet and not x==0 for x in playerBetsIn):
                return sum(playerBets)
        #If everyone's bet is the same by the last turn (they all checked) end the round
        if all(x==currentBet for x in playerBetsIn):
            return sum(playerBets)

def game(players):
    pass

#Testing
print(round(makePlayers(3)))

