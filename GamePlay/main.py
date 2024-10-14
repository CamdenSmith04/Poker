import sys
sys.path.insert(1, "Poker")

import BestHand.createDeck as cD
from player import Player
from pot import Pot
from gameRules import GameRules
from gameRules import Blinds
from table import Table
from linkedList import LinkedList
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

                    playersLL.insertAtEnd(Player(player_name, initial_deposit, [], 0))
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
            print("That is not a valid response")


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
    while inter.next:
        inter = inter.next
    inter.next = playersLL.head
    inter.next.next = None

    shiftedLL = inter.head
    shiftedLL.printLL()
    



    # Creates a new deck and shuffles it
    deck = cD.createDeck()
    random.shuffle(deck)
    # Players bet blinds
    actions.blinds(playersT, rules.blinds.small, rules.blinds.big, pot)
    # New player list is made with deck of cards
    new_players, new_deck = deal_cards(playersT, deck)
    # Second card is dealt
    deal_cards(new_players,new_deck)
    # Table is created with all players playing, the pot of 0, the top bet being the blind, and all players who haven't folded
    table = Table(new_players, pot, rules.blinds.big, new_players)
    # Check that prints players, balance, and hands
    for player in table.players:
          print(player.initialize())
    # Determines who is "under-the-gun" and bets first
    # if len(table.players) > 2:
    #     utg = table.players[2]
    # else:
    #     utg = table.players[0]
    
    playerLL = LinkedList()

    for player in table.players:
        playerLL.insertAtEnd(player.name)

    playerLL.printLL()


def checkBetFold(players, top_bet):
    return

# Helps print out players and their hands
def playersList(players):
    list = []
    for player in players:
        list.append([player.name, player.balance, player.hand])
    return list

# Deals cards to players by popping from the top of the deck
def deal_cards(players,deck):
    playersHand = []
    for player in players:
        player.hand.append(deck.pop())
        playersHand.append(Player(player.name, player.balance, player.hand, 0))

    print(playersList(playersHand))

    return players, deck

# Cycles through the orders of the players - First goes to last, second goes to first
def round_order(players):
    temp = []
    for i in range(1,len(players)):
        temp.append(players[i])
    temp.append(players[0])
    return temp

    
    


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
            

