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
    inter = LinkedList()
    inter.head = playersLL.head.next
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
    table = Table(inter, pot, rules.blinds.big, inter)
    # Check that prints players, balance, and hands
    print("------------------")
    inter.printLL()
    print("------------------")

    utg = inter.head.next.next

    if checkBetFold(utg, table.round_bet) == 9:
        inter.remove(utg)
        inter.printLL()
    else:
        inter.printLL()

def checkBetFold(player, top_bet):
    bool = False
    while(not bool):
        try:
            print("\nPLAYER ACTION REQUIRED\n")
            print(player.data.initialize())
            print(f"\nTop Bet: ${top_bet}")
            keyPress = int(input("1. Check\n2. Bet\n3. Fold "))
            match(keyPress):
                case 1:
                    # Check
                    if player.data.current_bet != top_bet:
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
                        return
                case 3:
                    # Fold
                    return 9


                case _:
                    print("Invalid input")
    
        except ValueError:
            print("Invalid Input")
    return

# Deals cards to players by popping from the top of the deck
def deal_cards(playersLL, deck):
    curr = playersLL.head
    while curr.next != playersLL.head:
        curr.data.hand.append(deck.pop())
        curr = curr.next
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
            

