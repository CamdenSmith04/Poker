import sys
sys.path.insert(1, "Poker")

import BestHand.createDeck as cD
from player import Player
from pot import Pot
from gameRules import GameRules
from gameRules import Blinds
from table import Table
from linkedList import Node, LinkedList
import actions
import random

SMALL_BLIND = 25
BIG_BLIND = 50

# This enables the game functions to be created
def create_game():
    playersLL = LinkedList()

    bool = False
    while(not bool):
        try:
            keyPress = int(input("Enter 1 To add a player. \nEnter 2 To start the game. \nEnter 3 To quit the game. "))
            match(keyPress):
                case 1:
                    player_name = input("Input player name: ")

                    x = False
                    while(not x):
                        try:
                            initial_deposit = int(input("Input initial deposit: "))
                            x = True
                        except ValueError:
                            print("Please enter a number.")

                    playersLL.insertAtEnd(Node(Player(player_name, initial_deposit, [], 0)))
                    playersLL.printLL()
            
                case 2:
                    print("Start game")

                    return playersLL

                case 3:
                    bool = True
                    return

                case _:
                    print("Invalid input")
        
        except ValueError:
            print("Invalid input")


# This is the main function
# <-//----------------------------------------------------------------//-->
def start_game(playersLL):
    new_round(playersLL, GameRules(blinds=Blinds(25,50))) # returns inter

    # Go through inter to get each rank
    # Compare ranks
    # Create tie function
    # Determine winner
    # Give winner pot, reset game, run again

    # If all folds already end game and new game, return inter escape

# <-//-----------------------------------------------------------------//->

def new_round(playersLL):
    pot = Pot(0)
    deck = cD.createDeck()
    random.shuffle(deck)
    deal_cards(playersLL, deck)
    deal_cards(playersLL, deck)
    roundLL = playersLL.head
    roundLL = roundLL.next
    roundLL.data.current_bet = SMALL_BLIND
    roundLL.data.balance -= SMALL_BLIND
    roundLL = roundLL.next
    roundLL.data.current_bet = BIG_BLIND
    roundLL.data.balance -= BIG_BLIND
    topBet = BIG_BLIND

    table = Table(pot, topBet, [])

    print(roundLL.data.initialize())

    print("------------------")
    playersLL.printLL()
    print("------------------")

    # PRE-FLOP BETTING
    #----------------------------------------//->
    roundLL = roundLL.next
    preFlopBetting(playersLL, roundLL, table, topBet)
    clearBets(playersLL, table)
    checkFolds(playersLL, table)

    print("-----------------------")
    playersLL.printLL()
    print()
    print(f"Pot: ${table.pot.size}")
    print("-----------------------")
    #----------------------------------------//->

    # CREATE FLOP
    #----------------------------------------//->
    deck.pop()
    for i in range(3):
        table.cards.append(deck.pop())

    print(f"Flop: {table.cards}")
    #----------------------------------------//->

    # FLOP BETTING
    #----------------------------------------//->
    table.topBet = 0
    round2LL = playersLL.head
    round2LL = round2LL.next
    postFlopBetting(playersLL, round2LL, table)
    clearBets(playersLL, table)
    checkFolds(playersLL, table)

    print("-----------------------")
    playersLL.printLL()
    print()
    print(f"Pot: ${table.pot.size}")
    print("-----------------------")
    #----------------------------------------//->

    # CREATE TURN
    #----------------------------------------//->
    deck.pop()
    table.cards.append(deck.pop())

    print(f"Turn: {table.cards}")
    #----------------------------------------//->

    # TURN BETTING
    #----------------------------------------//->
    table.topBet = 0
    round3LL = playersLL.head
    round3LL = round3LL.next
    postFlopBetting(playersLL, round3LL, table)
    clearBets(playersLL, table)
    checkFolds(playersLL, table)

    print("-----------------------")
    playersLL.printLL()
    print()
    print(f"Pot: ${table.pot.size}")
    print("-----------------------")
    #----------------------------------------//->

    # CREATE RIVER
    #----------------------------------------//->
    deck.pop()
    table.cards.append(deck.pop())

    print(f"River: {table.cards}")
    #----------------------------------------//->

    # RIVER BETTING
    #----------------------------------------//->
    table.topBet = 0
    round4LL = playersLL.head
    round4LL = round4LL.next
    postFlopBetting(playersLL, round4LL, table)
    clearBets(playersLL, table)
    checkFolds(playersLL, table)

    print("-----------------------")
    playersLL.printLL()
    print()
    print(f"Pot: ${table.pot.size}")
    print("-----------------------")
    #----------------------------------------//->

    return inter

def preFlopBetting(players, player, table, topBet):
    while player.data.current_bet != table.topBet:
        if checkBetFoldCall(player, table) == 9:
            players.remove(player)
        player = player.next
    if player.data.current_bet == table.topBet and table.topBet == topBet:
        if checkBetFoldCall(player, table) == 7:
            player = player.next
            preFlopBetting(players, player, table, topBet)


def postFlopBetting(players, player, table):
    if checkBetFoldCall(player, table) == 7:
        player = player.next
        while player.data.current_bet != table.topBet:
            if checkBetFoldCall(player, table) == 9:
                players.remove(player)
            player = player.next
    else:
        player = player.next
        while player.prev != players.head:
            preFlopBetting(players, player, table, table.topBet)
            player=player.next
    
            

def checkFolds(players, table):
    player = players.head
    if player == player.next:
        player.data.balance += table.pot.size
        table.pot.size = 0
    return

def clearBets(players, table):
    player = players.head
    table.pot.size += player.data.current_bet
    player.data.current_bet = 0
    player = player.next
    while (player != players.head):
        table.pot.size += player.data.current_bet
        player.data.current_bet = 0
        player = player.next
    return

def checkBetFoldCall(player, table):

    bool = False
    while(not bool):
        try:
            print("\nPLAYER ACTION REQUIRED")
            print(player.data.initialize())
            print(f"\nTop Bet: ${table.topBet}")
            keyPress = int(input("1. Check\n2. Bet\n3. Call\n4. Fold"))
            match(keyPress):
                case 1:
                    # Check
                    if player.data.current_bet != table.topBet:
                        print("\nERROR: You can't check.")
                    else:
                        return
                case 2:
                    # Bet
                    bet_amount = int(input("How much would you like to bet? "))
                    if bet_amount > player.data.balance:
                        print("\nERROR: You can't bet that much")
                    elif bet_amount < player.data.current_bet + table.topBet:
                        print("\nERROR: You must bet more than the current highest bet.")
                    else:
                        player.data.balance -= bet_amount
                        player.data.current_bet += bet_amount
                        table.topBet = player.data.current_bet
                        return 7
                    
                case 3:
                    # Call
                    if player.data.current_bet == table.topBet:
                        print("\nERROR: You are bidding the current bid, please check.")
                    else:
                        player.data.balance -= (table.topBet - player.data.current_bet)
                        player.data.current_bet = table.topBet
                        return 8

                case 4:
                    # Fold
                    table.pot.size += player.data.current_bet
                    player.data.current_bet = 0
                    return 9


                case _:
                    print("Invalid input")
    
        except ValueError:
            print("Invalid Input")
    return

# Deals cards to players by popping from the top of the deck
def deal_cards(LL, deck):
    curr = LL.head
    curr.data.hand.append(deck.pop())
    curr = curr.next
    while curr != LL.head:
        curr.data.hand.append(deck.pop())
        curr = curr.next
    return

def add_card(table, deck):
    deck.pop()
    table.cards.append(deck.pop())
    return

# This begins the output the user sees
print("Welcome to Poker Simulator!")

bool = False
while(not bool):
    keyPress = input("To begin type 'Start' to quit type 'Quit'\n")
    match(keyPress):
        case "Start":
            # Add input here to change what the blinds are
            start_game(create_game())
            break
        case "Quit":
            bool = True
            break
        case _:
            print("Invalid input")
            

