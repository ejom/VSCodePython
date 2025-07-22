from collections import Counter
import random

class Cards:
    def __init__(self):
        suits = ["Hearts", "Clubs", "Diamonds", "Spades"]
        ranks = list(range(1, 14))
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append((rank, suit))
    def draw(self, amount=1):
        cards = self.deck[:amount]
        del self.deck[:amount]
        return cards
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
        self.folded = False
        self.totalBet = 0
        self.roundBet = 0
        self.hand = []
        self.sidePot = 0

    def __str__(self):
        return f"{self.name} has {self.money} left."
    def bet(self, amount):
        if self.money >= amount:
            self.money -= amount
            if self.money == 0:
                self.allIn = True
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
                print("You don't go all-in. You must fold")
                self.folded=True
                return 0


def makePlayers(numPlayers, startMoney=0):
    players = list(range(numPlayers))
    #TESTING
    presetNames = ["Jake", "Paul", "Mike", "Alice", "Mark"]
    presetMoney = [30, 50, 70, 50, 80]
    for i in range(numPlayers):
        while True:
            try:
                #name = input(f"Enter the name for player {i+1}: ")
                name = presetNames[i]
                #TESTING custom moneys
                #money = startMoney if startMoney else int(input("Enter your starting cash: "))
                money = presetMoney[i]
                break
            except:
                print("Invalid input. Try again.")
        players[i] = Player(name, money)
    print("Players recap:")
    print(*players)
    return players

def betRound(players, minBet=0):
    currentBet=minBet
    roundNum = 0

    #Make sure the round bet for the round is reset
    for player in players:
        player.roundBet = 0

    while True:
        roundNum += 1
        for i, player in enumerate(players):
            #Overview and determine if game or round is over
            #See if there's only one player left
            playersIn = [person for person in players if not person.folded]
            for person in [person for person in players if person.allIn]:
                    if person.totalBet > currentBet:
                        currentBet = person.totalBet
            if sum(not (person.folded or person.allIn) for person in players) <= 1:
                maxBet = max(person.totalBet for person in players if not person.folded)
                if all((person.totalBet == maxBet or (person.allIn and person.totalBet <= maxBet)) for person in playersIn):
                    for player in players:
                        for nPlayer in players:
                            if nPlayer.roundBet > player.roundBet:
                                player.sidePot += player.roundBet
                            else:
                                player.sidePot += nPlayer.roundBet
                    #Update their total bet
                    print("We can determine a winner")
                    return sum(player.roundBet for player in players), True
            
            print(f"\n"+"_"*20)
            print(*players)
            for person in players:
                print(f"{person.name} has bet {person.roundBet}")
            #build an array of everyone's current bet that is still in
            playerBetsIn = [person.roundBet for person in players if not person.folded and not person.allIn]
            #As long as its not the first turn, we end the betRound if everyone's bet is the same
            if all(x==currentBet for x in playerBetsIn) and roundNum > 1:
                for player in players:
                    for nPlayer in players:
                        if nPlayer.roundBet > player.roundBet:
                            player.sidePot += player.roundBet
                        else:
                            player.sidePot += nPlayer.roundBet
                #Update their total bet
                return sum(player.roundBet for player in players), False

            #If you arent in (folded or all in) you dont get a turn
            if player.folded or player.allIn:
                continue

            #If you are big or small blind (round 1 with an ante) you auto bet the ante and continue
            if minBet > 0:
                if roundNum == 1 and i == 0:
                    player.roundBet += player.bet(minBet)
                    continue
                if roundNum == 1 and i == 1:
                    player.roundBet += player.bet(int(minBet/2))
                    continue

            print()
            print("-"*20+f"{players[i].name}'s turn"+"-"*20)
            input("Press Enter to reveal hand and start turn")
            print(player.hand)
            #Recap the currentBet and player's bet
            print(f"Your bet so far is ${player.roundBet}. The current bet on the pot is ${currentBet}")
            #Determine if the player can bet/check or if they need to match/raise/fold
            #bet/check
            if player.roundBet == currentBet:
                print("You can bet (enter a number>0) or check (enter 0 or nothing)?")
                while True:
                    try:
                        choice = input("Enter how much to raise the current bet (int): ")
                        if not choice:
                            x = 0
                        else:
                            x = int(choice)
                        break
                    except:
                        print("Invalid input. Try again.")
                player.roundBet += player.bet(x)
                currentBet = player.roundBet
            #match/raise/fold
            else:
                print("Would you like to raise/match the current bet or fold?")
                print(f"To meet the current bet you must enter at least {currentBet-player.roundBet}. If you are going all in just enter the minimum bet")
                while True:
                    try:
                        choice = input("Enter f for fold or enter the amount of your bet for raise/match: ")
                        #Bet the minimum by default
                        if not choice:
                            x = currentBet-player.roundBet
                        else:
                            #Make sure they are betting an int
                            x = int(choice)
                        #Make sure they bet the minimum to match
                        if x < currentBet-player.roundBet:
                            print("Bet is lower than the minimum bet")
                            raise Exception("Bet is lower than the minimum bet")
                        player.roundBet += player.bet(x)
                        break
                    except:
                        #If its not a number than the player's input is either folding or invalid
                        #Folding
                        if choice[0].lower() == 'f':
                            print("You folded")
                            player.folded = True
                            break
                        #Invalid, stuck in while loop until valid input is given (f or big enough number)
                        print(f"This is either an invalid input or below {currentBet-player.roundBet}. Try again")
                #if the player is all-in is similar process to folding.
                if player.allIn:
                    continue
                #Get out of the for loop immediately if the player folded and move to next player
                if player.folded:
                    continue
                #Once we determine that the raise is valid add it to their current bet. 
                currentBet = player.roundBet


def game(players, ante):
    #IMPLEMENT: totalBet updating
    #Setup the deck
    cards = Cards()
    #Make this more random?
    cards.shuffle()

    #Initialize player's stuff
    for player in players:
        player.allIn = False
        player.folded = False
        player.totalBet = 0
        # deal cards
        #TESTING: custom hand
        #player.hand += (cards.draw(2))
    #TESTING: custum card hand
    customHands = [[(1, 'Hearts'), (2, 'Spades')], [(1, 'Hearts'), (2, 'Spades')], [(1, 'Hearts'), (2, 'Spades')], [(1, 'Hearts'), (2, 'Spades')], [(1, 'Hearts'), (2, 'Spades')]]
    for i, player in enumerate(players):
        player.hand += customHands[i]
    
    pot = 0
    #TESTING: Custom river
    #river = []
    river = [(3, 'Hearts'), (4, 'Spades'), (5, 'Hearts'), (11, 'Hearts'), (12, 'Spades')]

    for i in range(4):
        print(f"\n"+"-"*60)
        if i == 0:
            print(f"This is the initial betRound with an ante of {ante}")
            print("Everyone gets two cards for their hand")
        elif i == 1:
            print("This is the river betRound. Three cards are revealed to everyone.")
            #river+= cards.draw(3)
            print(river)
        elif i==2:
            print("This is the 3rd betRound. An additional card is revealed.")
            #river += cards.draw()
            print(river)
        else:
            print("This is the final betRound. One last card is revealed.")
            #river += cards.draw()
            print(river)
        print("-"*60+f"\n")
        potGain, gameOver = betRound(players, minBet = ante if i==0 else 0)
        pot += potGain

        #Recap the pot
        print("-"*60)
        print(f"pot is at {pot}")
        for player in players:
            print(f"{player.name} has a total bet of {player.totalBet}")
        print("-"*60)

        if gameOver:
            if len(river) < 5:
                river += cards.draw(5-len(river))
            finishGame(pot, river, players=[player for player in players if not player.folded])
            return
    finishGame(pot, river, players=[player for player in players if not player.folded])
    return

def finishGame(pot, river, players):
    #Compares the cards of players who havent folded. 
    #Distributes pot to player's money based on who has the best hand and if the winner was all in
    #If the player wasn't all in they get the whole pot

    #If they were all in then they get their total bet for that betRound*num of not folded players
    #The remaining pot gets distributed evenly to the participating nonfolded players. 

    #For testing determine a random player as the winner
    print(f"The pot is {pot}")
    print("We reveal the cards!") 

    print(f"The river is:\n{river}")
    for player in players:
        print(f"{player.name}'s cards are {player.hand}")

    winners, winningSet = winningHand(river, players)

    if len(winners)==1:
        print(f"the winner is: {winners[0].name} with a {winningSet}. Their hand was {winners[0].hand}")
    else:
        print("We have a Tie!")
        print(f"The winners are: {[player.name for player in winners]}")
    #all-in caveats
    if not any(winner.allIn for winner in winners):
        for winner in winners:
            winner.money += int(pot/len(winners))
    else:
        losers = []
        for loser in [player for player in players if player not in winners]:
            losers.append(loser)
        winners.sort(key= lambda x: x.totalBet)
        
        j = 0
        for i, winner in enumerate(winners):
            if i != 0:
                if winner.totalBet > winners[i-1].totalBet:
                    #If the winner had a bigger side pot increment this so they dont split it with lesser i before
                    j=i
                    #Bigger winners just split the remaining pot
                    winner.sidePot -= winners[i-1].sidePot
                else:
                    #Same winners already got their winnings
                    continue
            #Take out the winners sidePot
            pot -= winner.sidePot
            #Split it among winners with greater or equal sidepots
            for nWinner in winners[j:]:
                nWinner.money += int(winner.sidePot/(len(winners)-j))
                    
    print(*players)
    
def winningHand(river, players):
    winnerPoints = 0
    #IMPLEMENT: Ties
    haveTie = False
    for player in players:
        playerHand = river + player.hand
        player.points, player.hand = handToPoints(playerHand)
    for i in range(len(players)):
        if players[i].points > winnerPoints:
            winnerPoints = players[i].points
            winner = [players[i]]
        elif players[i].points == winnerPoints:
            winner.append(players[i])
    if winner[0].points < 1e10:
        setName = "High Card"
    elif winner[0].points < 2e10:
        setName = "Pair"
    elif winner[0].points < 3e10:
        setName = "Two Pair"
    elif winner[0].points < 4e10:
        setName = "Three of a Kind"
    elif winner[0].points < 5e10:
        setName = "Straight"
    elif winner[0].points < 6e10:
        setName = "Flush"
    elif winner[0].points < 7e10:
        setName = "Full House"
    elif winner[0].points < 8e10:
        setName = "Four of a Kind"
    else:
        setName = "Straight Flush"
    return winner, setName

def handToPoints(hand):
    #places needed: hand = 1, handset = 2, HighCards = 2
    #Worst case scenerio is high card
    #High card: hand + highcard*5 = 1+5*2 = 11

    #Extract suits and ranks--sort from high rank to low rank
    #For each distincy rank in the hand store the count
    ranks = []
    suits = []
    for card in hand:
        ranks.append(card[0])
        suits.append(card[1])

    #Sort ranks to be from high frequency to low frequency, and then from high card to low card
    freqDict = (Counter(ranks))
    ranks = sorted(ranks, key=lambda count: (-freqDict[count], -count))

    handDict = Counter(rank for rank, suit in hand)
    hand = sorted(hand, key=lambda card: (-handDict[card[0]], -card[0]))
    winningHand = hand[:5]

    #Check for straightFlush
    if max(Counter(suits).values()) >= 5:
        #Extract cards of the same most common suit
        nHand = [card for card in hand if Counter(suits).most_common(1)[0][0] in card]
        #Resort from high to low rank
        nHand.sort(reverse=True)
        isStraightFlush, winningHand = isSequentialHand(nHand, hand)
        if isStraightFlush:
            #Straight Flush
            points = 8e10
            points += winningHand[0][0]
            return int(8e10), winningHand
        else:
            winningHand = hand[:5]
            print(winningHand)
    
    #If the first four are the same its a 4 of a kind (since its already sorted high to low freq)
    if len(set(ranks[:4])) == 1:
        #Four of a kind
        points = int(7e10)
        points += ranks[0] * int(1e2)
        points += ranks[4]
        return points, winningHand
    
    #Test top 3 for three of a kind
    isThreeOfKind = False
    if len(set(ranks[:3])) == 1:
        isThreeOfKind = True
        #After the first three are confirmed together (and we already know its not four of a kind) we can test the next two
        if len(set(ranks[3:5])) == 1:
            #Full house
            points = int(6e10)
            points += ranks[0] * int(1e2)
            points += ranks[3]
            return points, winningHand

    #If the max count of same suits at least 5 we have flush
    if max(Counter(suits).values()) >= 5:
        #Flush
        handDict = Counter(suit for rank, suit in hand)
        hand = sorted(hand, key=lambda card: (-handDict[card[1]], -card[0]))
        winningHand = hand[:5]

        points = int(5e10)
        points += winningHand[0][0]
        return int(5e10), winningHand
    #Testing for straight again, sorting hand by just order 
    nHand = sorted(hand, reverse=True)
    isStraight, winningHand = isSequentialHand(nHand, hand)
    if isStraight: 
        #Straight
        points = int(4e10)
        points += winningHand[0][0]
        return int(4e10), winningHand
    else:
        winningHand = hand[:5]
    # if three of a king was true return three of a kind. 
    if isThreeOfKind:
        #Three of a kind
        points = int(3e10)
        points += ranks[0] * int(1e4)
        points += ranks[3] * int(1e2)
        points += ranks[4] 
        return points, winningHand
    # Test top 4 for 2-pair
    if ranks[0]==ranks[1] and ranks[2]==ranks[3]:
        #Two Pair has 2e6 points (also initialize it here)
        points = int(2e10)
        #Add highest pair rank to next place
        points += ranks[0] * int(1e4)
        #In case of ties evaluate the second highest pair
        points += ranks[2] * int(1e2)
        #Finally take into account the high card
        points += ranks[4]
        #Two Pair
        return points, winningHand
    #Test top 2 for pair
    if ranks[0]==ranks[1]:
        #Calculate the points
        points = int(1e10)
        #Pair takes priority
        points += ranks[0] * int(1e6)
        #Than three high cards
        for i in range(len(ranks[2:])):
            points += ranks[i+2] * int(10**(4-2*i))
        return points, winningHand

    #default return the highest card
    #Calculate points
    points = int(0)
    for i in range(len(ranks)):
        points += ranks[i] * int(10**(8-2*i))
    return points, winningHand

def isSequentialHand(hand, winningHand):
    n=0
    nWinningHand = [hand[0]]
    for i in range(1, len(hand)):
        if (hand[i][0] - hand[i-1][0] == -1):
            n+= 1
            nWinningHand.append(hand[i])
            if n >= 4:
                return True, nWinningHand
        elif hand[i][0] - hand[i-1][0] == 0:
            pass
        else:
            nWinningHand = [hand[i]]
            n=0
    return False, winningHand

#Testing
players = makePlayers(5)
game(players, 5)

