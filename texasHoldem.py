import random

#Texas holdem poker game by Ethan Olsen
# This game will function like a pass and play game. New lines will be printed to "clear" the terminal. 
# Create a deck of cards
#objects
class Game:
    deck = ((rank, suit) for rank in range(1, 14) for suit in range(1, 5))
    def shuffle(self):
        self.deck = ((rank, suit) for rank in range(1, 14) for suit in range(1, 5))
        random.shuffle(self.deck)
    card = {
        (1, 1): "Ace of Spades",
        (2, 1): "2 of Spades",
        (3, 1): "3 of Spades",
        (4, 1): "4 of Spades",
        (5, 1): "5 of Spades",
        (6, 1): "6 of Spades",
        (7, 1): "7 of Spades",
        (8, 1): "8 of Spades",
        (9, 1): "9 of Spades",
        (10, 1): "10 of Spades",
        (11, 1): "Jack of Spades",
        (12, 1): "Queen of Spades",
        (13, 1): "King of Spades",
        (1, 2): "Ace of Hearts",
        (2, 2): "2 of Hearts",
        (3, 2): "3 of Hearts",
        (4, 2): "4 of Hearts",
        (5, 2): "5 of Hearts",
        (6, 2): "6 of Hearts",
        (7, 2): "7 of Hearts",
        (8, 2): "8 of Hearts",
        (9, 2): "9 of Hearts",
        (10, 2): "10 of Hearts",
        (11, 2): "Jack of Hearts",
        (12, 2): "Queen of Hearts",
        (13, 2): "King of Hearts",
        (1, 3): "Ace of Clubs",
        (2, 3): "2 of Clubs",
        (3, 3): "3 of Clubs",
        (4, 3): "4 of Clubs",
        (5, 3): "5 of Clubs",
        (6, 3): "6 of Clubs",
        (7, 3): "7 of Clubs",
        (8, 3): "8 of Clubs",
        (9, 3): "9 of Clubs",
        (10, 3): "10 of Clubs",
        (11, 3): "Jack of Clubs",
        (12, 3): "Queen of Clubs",
        (13, 3): "King of Clubs",
        (1, 4): "Ace of Diamonds",
        (2, 4): "2 of Diamonds",
        (3, 4): "3 of Diamonds",
        (4, 4): "4 of Diamonds",
        (5, 4): "5 of Diamonds",
        (6, 4): "6 of Diamonds",
        (7, 4): "7 of Diamonds",
        (8, 4): "8 of Diamonds",
        (9, 4): "9 of Diamonds",
        (10, 4): "10 of Diamonds",
        (11, 4): "Jack of Diamonds",
        (12, 4): "Queen of Diamonds",
        (13, 4): "King of Diamonds",
    }
    nPlayers = 0
    players = []
    startingChips = 0
    maxCycles = 0
    ante = 5
    haveWinner = False

class Player:
    def __init__(self, name):
        self.name = name
        self.chips = Game.startingChips
    cards = [(0, 0), (0, 0)]
    def bet(self, amount):
        if self.chips < amount:
            print("You are all in")
            amount = self.chips
        self.chips -= amount
        self.curBet += amount
        print(f"You bet {amount} chips. You have {self.chips} chips remaining.")
    def draw(self):
        self.cards[0] = random.choice(Game.deck)
        Game.deck.remove(self.cards[0])
        self.cards[1] = random.choice(Game.deck)
        Game.deck.remove(self.cards[1])
    fold = False
    curBet = 0

#Functions
def setup():
    #determine number of players
    while (True):
        nPlayers = input("Please enter the number of players (only the number, must be at least 2):")
        try:
            Game.nPlayers = int(nPlayers)
            if Game.nPlayers < 2:
                print("Invalid input. Must have at least 2 players.")
                continue
            break
        except:
            print("Invalid input. Please enter a number.")
    #determine starting chips
    while (True):
        startingChips = input("Please enter the number of starting chips (only the number):")
        try:
            Game.startingChips = int(startingChips)
            if Game.startingChips < 5:
                print("Invalid input. Must have at least 5 chips.")
                continue
            break
        except:
            print("Invalid input. Please enter only a number.")
    #determine names of players
    for i in range(Game.nPlayers):
        name = input(f"Please enter the name of player {i+1}:")
        Game.players.append(Player(name))
    #determine number of rounds
    while (True):
        maxCycles = input("Please enter the number of cycles (only the number). 1 cycle occers after each player plays a hand. If you wish to play until only one player has chips, enter 0:")
        try:
            Game.maxCycles = int(maxCycles)
            break
        except:
            print("Invalid input. Please enter only a number.")
#Script
setup()
cycle = 1
hand = 1
#For each hand
while True:
    if (cycle>Game.maxCycles and Game.maxCycles !=0) or Game.haveWinner:
        endGame()
        break
    else: 
        playHand(Game(), hand)
        if hand>=Game.nPlayers:
            hand = 1
            if Game.maxCycles != 0:
                cycle += 1
            # The ante will start at 5c and will double each cycle 
            Game.ante *= 2
        else:
            hand += 1

def playTurn(Game, hand, round, tBet, i):
    player = Game.players
    input(f"It is {player[i].name}'s turn. Press enter when you are ready.")
    print(f"Your cards are {Game.card[player[i].cards[0]]} and {Game.card[player[i].cards[1]]}.")
    if (round==0 and i==hand):
        print("Since you are the big blind, you must bet the ante")
        tBet += player[i].bet(Game.ante)
    else:
        print(f"The current bet is {tBet}.")
        if tBet == 0:
            action = input("Do you want to check (0) or bet (1)?")
            if action == '1':
                while True:
                    bet = input("How much do you want to bet?")
                    try:
                        bet = int(bet)
                        tBet += player[i].bet(bet)
                        break
                    except:
                        print("Invalid input. Please enter only a number.")
        else:
            action = input("Do you want to call/raise (1) or fold (0)?")
            if action == '1':
                while True:
                    nRaise = input("Enter the amount you would like to raise (>=0). If you call, enter 0")
                    try: 
                        nRaise = int(nRaise)
                        if nRaise < 0:
                            continue
                        tBet += player[i].bet(tBet+nRaise-player[i].curBet)
                        break
                    except:
                        print("Invalid input. Please enter only a number.")
            else:
                player[i].fold = True

def playRound(Game, hand, round):
    tBet = 0
    player = Game.players
    for i in range(Game.nPlayers):
        player[i].curBet = 0
    #each turn
    for i in [list(range(hand, Game.nPlayers))+list(range(0, hand))]:
        if not player[i].fold:
            playTurn(Game, hand, round, tBet, i)

def playHand(Game, hand):
    #decide ante, dealer, and blinds
    player = Game.players
    print(f"{player[hand-1].name} is the dealer.")
    print(f"{player[hand].name} is the big blind.")
    pot = 0
    #everyone draws cards
    for i in range(Game.nPlayers):
        #draw 2 cards
        player[i].draw()
    #for each round
    for round in range(5):
        playRound(Game, hand, round)

    # Round 1
    # Round 2 
    # Reveal 3 cards to each player
    # for each turn
    #reveal your cards
    # Bet or check/fold

    # Round 3
    # Reveal 4th card
    # for each turn
    #reveal your cards
    # Bet or check/fold

    # Round 4
    # Reveal 5th card
    # for each turn
    #reveal your cards
    # Bet or check/fold

    # Round 5
    # for each turn
    #reveal your cards
    # Bet or check/fold

    # Reveal remaining players' cards
    # Determine the winner
    # award winner with pot
    #Anyone with no chips is out