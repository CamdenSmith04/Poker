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
    new_round(playersLL, GameRules(blinds=Blinds(25,50)))
    
    
    

# <-//-----------------------------------------------------------------//->

def new_round(playersLL, rules):
    # Sets pot size to 0
    pot = Pot(0)
    # Rotates players by 1
    rotatedLL = LinkedList()
    rotatedLL.head = playersLL.head.next
    # Creates the list that will track folds
    inter = LinkedList()
    inter.head = rotatedLL.head
    # Creates a new deck and shuffles it
    deck = cD.createDeck()
    random.shuffle(deck)
    # Players bet blinds
    actions.blinds(inter, rules.blinds.small, rules.blinds.big, pot)
    # New player list is made with deck of cards
    deal_cards(inter, deck)
    # Second card is dealt
    deal_cards(inter, deck)
    # Table is created with all players playing, the pot of 0, the top bet being the blind, and all players who haven't folded
    table = Table(inter, pot, rules.blinds.big, inter, [])
    # Check that prints players, balance, and hands
    print("------------------")
    inter.printLL()
    print("------------------")

    # Head is the biggest bet (big blind)
    inter.head = inter.head.next

    # Next players turn - after big blind
    pTurn = inter.head.next

    while (pTurn != inter.head):
        x = checkBetFoldCall(pTurn, table)
        if x == 9:
            inter.remove(pTurn)
            pTurn = pTurn.next
        elif x == 7:
            inter.head = pTurn
            pTurn = pTurn.next
        elif x == 8:
            pTurn = pTurn.next
        else:
            pTurn = pTurn.next

    # Make function to let big blind bet if all call/check

    # Adds pot size and clears bets
    pTurn = inter.head
    table.pot.size += pTurn.data.current_bet
    pTurn.data.current_bet = 0
    pTurn = pTurn.next
    while (pTurn != inter.head):
        table.pot.size += pTurn.data.current_bet
        pTurn.data.current_bet = 0
        pTurn = pTurn.next
    

    if pTurn == pTurn.next:
        pTurn.data.balance += pot.size
        pot.size = 0
        # New Round functions

    inter.printLL()

    print(f"\nPot: ${table.pot.size}\n")

    flop(table, deck)
    print(f"Flop: {table.cards}")

    # For turn
    p1Turn = inter.head

    # -------------- # -------------- # -------------- # -------------- # -------------- #
    # | Add functionality to count for first person being able to make an action       | #
    # -------------- # -------------- # -------------- # -------------- # -------------- #
    while (p1Turn != inter.head):
        x = checkBetFoldCall(p1Turn, table)
        if x == 9:
            inter.remove(p1Turn)
            p1Turn = p1Turn.next
        elif x == 7:
            inter.head = p1Turn
            p1Turn = p1Turn.next
        elif x == 8:
            p1Turn = p1Turn.next
        else:
            p1Turn = p1Turn.next

    p1Turn = inter.head
    table.pot.size += p1Turn.data.current_bet
    p1Turn.data.current_bet = 0
    p1Turn = pTurn.next
    while (p1Turn != inter.head):
        table.pot.size += p1Turn.data.current_bet
        p1Turn.data.current_bet = 0
        p1Turn = p1Turn.next
    

    if p1Turn == p1Turn.next:
        p1Turn.data.balance += pot.size
        pot.size = 0

    inter.printLL()

    print(f"\nPot: ${table.pot.size}\n")

    add_card(table, deck)
    print(f"Flop: {table.cards}")


    
    return rotatedLL
    # For river

def checkBetFoldCall(player, table):

    bool = False
    while(not bool):
        try:
            print("\nPLAYER ACTION REQUIRED")
            print(player.data.initialize())
            print(f"\nTop Bet: ${table.round_bet}")
            keyPress = int(input("1. Check\n2. Bet\n3. Call\n4. Fold"))
            match(keyPress):
                case 1:
                    # Check
                    if player.data.current_bet != table.round_bet:
                        print("You can't check.")
                    else:
                        return
                case 2:
                    # Bet
                    bet_amount = int(input("How much would you like to bet? "))
                    if bet_amount > player.data.balance:
                        print("You can't bet that much")
                    else:
                        player.data.balance -= bet_amount
                        player.data.current_bet += bet_amount
                        table.round_bet = bet_amount
                        
                        return 7
                    
                case 3:
                    # Call
                    player.data.balance -= (table.round_bet - player.data.current_bet)
                    player.data.current_bet = table.round_bet
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
def deal_cards(playersLL, deck):
    curr = playersLL.head
    curr.data.hand.append(deck.pop())
    curr = curr.next
    while curr != playersLL.head:
        curr.data.hand.append(deck.pop())
        curr = curr.next
    return

def flop(table, deck):
    deck.pop()
    for i in range(3):
        table.cards.append(deck.pop())
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
            

