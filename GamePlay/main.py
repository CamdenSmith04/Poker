# Import Additional Folder in Poker - "BestHand"
import sys
sys.path.insert(1, "Poker")

# Imports
import BestHand.createDeck as cD
import BestHand.bestHand as bH
import BestHand.decodeHand as decode
from player import Player
from pot import Pot
from table import Table
from linkedList import Node, LinkedList
import random

# Global variables
SMALL_BLIND = 25
BIG_BLIND = 50

def create_game():
    # Creates empty linked list that will determine player order at table
    playersLL = LinkedList()
    bool = False
    while(not bool):
        try:
            # Allows user to add players, begin the game, or quit it all together
            # TODO ADD FUNCTIONALITY TO ENABLE MULTI ROUNDS AS LONG AS LIST > 1 PLAYER
            keyPress = int(input("Enter 1 To add a player. \nEnter 2 To start the game. \nEnter 3 To quit the game. "))
            match(keyPress):
                # Add Player
                case 1:
                    player_name = input("Input player name: ")
                    x = False
                    while(not x):
                        try:
                            initial_deposit = int(input("Input initial deposit: "))
                            x = True
                        except ValueError:
                            print("Please enter a number.")
                    # Add player to end of player Linked List
                    playersLL.insertAtEnd(Node(Player(player_name, initial_deposit, [], 0)))
                    playersLL.printLL()
                # Start a New Round
                case 2:
                    print("Start round")
                    return playersLL
                # Quit Game
                case 3:
                    bool = True
                    break
                # Other inputs
                case _:
                    print("Invalid input")
        # Invalid inputs
        except ValueError:
            print("Invalid input")
    
def new_round(playersLL):
    # Creates new game state for round
    pot = Pot(0)
    deck = cD.createDeck()
    random.shuffle(deck)

    # Deals first two cards
    deal_cards(playersLL, deck)
    deal_cards(playersLL, deck)

    # Dealer is head of LL
    roundLL = playersLL.head
    roundLL = roundLL.next
    # Small Blind is next
    roundLL.data.current_bet = SMALL_BLIND
    roundLL.data.balance -= SMALL_BLIND
    roundLL = roundLL.next
    # Big Blind is next
    roundLL.data.current_bet = BIG_BLIND
    roundLL.data.balance -= BIG_BLIND

    # Create table class with pot of zero and biggest bet of BIG_BLIND
    table = Table(pot, BIG_BLIND, [])

    # PRE-FLOP BETTING
    #----------------------------------------//->
    roundLL = roundLL.next
    preFlopBetting(playersLL, roundLL, table, BIG_BLIND)
    clearBets(playersLL, table)
    checkFolds(playersLL, table)

    print()
    print("-----------------------")
    print(f"Pot: ${table.pot.size}")
    print("-----------------------")
    print()
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

    print()
    print("-----------------------")
    print(f"Pot: ${table.pot.size}")
    print("-----------------------")
    print()
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

    print()
    print("-----------------------")
    print(f"Pot: ${table.pot.size}")
    print("-----------------------")
    print()
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

    print()
    print("-----------------------")
    print(f"Pot: ${table.pot.size}")
    print("-----------------------")
    print()
    #----------------------------------------//->

    determineWinner(handRank(playersLL, table), pot)
    
    playersLL.printLL()

    return playersLL

def handRank(players, table):
    print("-----------------------")
    print("Top Hands")
    print("-----------------------")

    # Adds player's first and second card to new list
    player = players.head
    allCards = []
    allCards.append(player.data.hand[0])
    allCards.append(player.data.hand[1])
    # Appends river to allCards list
    for i in range(len(table.cards)):
        allCards.append(table.cards[i])
    # Clears out existing player hands and appends their best hand to their hand
    player.data.hand = []
    player.data.hand.append(bH.best_hand(decode.decode(allCards))[0])
    print(player.data.hand)
    player = player.next
    while player != players.head:
        # Adds player's first and second card to new list
        allCards = []
        allCards.append(player.data.hand[0])
        allCards.append(player.data.hand[1])
        # Appends river to allCards list
        for i in range(len(table.cards)):
            allCards.append(table.cards[i])
        # Clears out existing player hands and appends their best hand to their hand
        player.data.hand = []
        player.data.hand.append(bH.best_hand(decode.decode(allCards))[0])
        print(player.data.hand)
        player = player.next
    return players

def determineWinner(players, pot):
    player = players.head
    top_rank = player.data.hand[-1][-1]
    print()
    print("-----------------------")
    print("Winner")
    print("-----------------------")
    # Keeps track of number of players tied for first
    player_count = 1
    # Begins comparing hands of current player to previous player
    player = player.next
    # While the player isn't the first player
    while player != players.head:
        # If the current players rank is lower (better)
        if player.data.hand[-1][-1] < top_rank:
            # Update the top rank
            top_rank = player.data.hand[-1][-1]
            # Remove the previous players tied for first
            player_count = removes(players, player, player_count)
        # If the current players rank is equal
        elif player.data.hand[-1][-1] == top_rank:
                # If both players have a royal flush
                if top_rank == 1:
                    # The number of players tied for first increases
                    player_count += 1

                # If both players have a straight flush or a straight
                elif top_rank == 2 or top_rank == 6:
                    # If the current player has the higher last card
                    if player.data.hand[0][0][0] > player.prev.data.hand[0][0][0]:
                        # Remove the previous players tied for first
                        player_count = removes(players, player, player_count)
                    # If the straight consists of the same cards
                    elif player.data.hand[0][0][0] == player.prev.data.hand[0][0][0]:
                        # The number of players tied for first increases
                        player_count += 1
                    else:
                        # Remove the current player if the previous card has a higher straight
                        players.remove(player)

                # If both players have four of a kind
                elif top_rank == 3:
                    if player.data.hand[0][1][0] > player.prev.data.hand[0][1][0]:
                        player_count = removes(players, player, player_count)
                    elif player.data.hand[0][1][0] == player.prev.data.hand[0][1][0]:
                        player_count += 1
                    else:
                        players.remove(player)
                
                # If both players have a full house
                elif top_rank == 4:
                    if player.data.hand[0][2][0] > player.prev.data.hand[0][2][0]:
                        player_count = removes(players, player, player_count)
                    elif player.data.hand[0][2][0] == player.prev.data.hand[0][2][0]:
                        if player.data.hand[0][0][0] > player.prev.data.hand[0][0][0]:
                            player_count = removes(players, player, player_count)
                        elif player.data.hand[0][0][0] == player.prev.data.hand[0][0][0]:
                            if player.data.hand[0][4][0] > player.prev.data.hand[0][4][0]:
                                player_count = removes(players, player, player_count)
                            elif player.data.hand[0][4][0] == player.prev.data.hand[0][4][0]:
                                player_count += 1
                            else:
                                players.remove(player)
                        else:
                            players.remove(player)
                    else:
                        players.remove(player)

                # If both players have three of a kind
                elif top_rank == 7:
                    if player.data.hand[0][2][0] > player.prev.data.hand[0][2][0]:
                        player_count = removes(players, player, player_count)
                    elif player.data.hand[0][2][0] == player.prev.data.hand[0][2][0]:
                        player1_cards = []
                        player2_cards = []

                        same = player.data.hand[0][2][0]

                        for i in range(len(player.data.hand[0])-1):
                            if player.data.hand[0][i][0] != same:
                                player1_cards.append(player.data.hand[0][i][0])
                        for i in range(len(player.prev.data.hand[0])-1):
                            if player.prev.data.hand[0][i][0] != same:
                                player2_cards.append(player.prev.data.hand[0][i][0])

                        player1_cards.sort()
                        player2_cards.sort()

                        if player1_cards[-1] > player2_cards[-1]:
                            player_count = removes(players, player, player_count)
                        elif player1_cards[-1] == player2_cards[-1]:
                            if player1_cards[0] > player2_cards[0]:
                                player_count = removes(players, player, player_count)
                            elif player1_cards[0] == player2_cards[0]:
                                player_count += 1
                            else:
                                players.remove(player)
                        else:
                            players.remove(player)
                    else:
                        players.remove(player)
                
                # If both players have a flush
                elif top_rank == 5:
                    i = 4
                    while i > -1:
                        if player.data.hand[0][i][0] > player.prev.data.hand[0][i][0]:
                            player_count = removes(players, player, player_count)
                            i = -1
                        elif player.data.hand[0][i][0] < player.prev.data.hand[0][i][0]:
                            players.remove(player)
                            i = -1
                        else:
                            i -= 1

                # If both players have a two pair
                elif top_rank == 8:
                    if player.data.hand[0][3][0] > player.prev.data.hand[0][3][0]:
                        player_count = removes(players, player, player_count)
                    elif player.data.hand[0][3][0] == player.prev.data.hand[0][3][0]:
                        if player.data.hand[0][1][0] > player.prev.data.hand[0][1][0]:
                            player_count = removes(players, player, player_count)
                        elif player.data.hand[0][1][0] == player.prev.data.hand[0][1][0]:
                            player1_card = 0
                            player2_card = 0
                            if player.prev.data.hand[0][0][0] == player.prev.data.hand[0][1][0] and player.prev.data.hand[0][3][0] == player.prev.data.hand[0][4][0]:
                                player1_card = player.prev.data.hand[0][2][0]
                            elif player.prev.data.hand[0][1][0] == player.prev.data.hand[0][2][0] and player.prev.data.hand[0][3][0] == player.prev.data.hand[0][4][0]:
                                player1_card = player.prev.data.hand[0][0][0]
                            else:
                                player1_card = player.prev.data.hand[0][4][0]

                            if player.data.hand[0][0][0] == player.data.hand[0][1][0] and player.data.hand[0][3][0] == player.data.hand[0][4][0]:
                                player2_card = player.data.hand[0][2][0]
                            elif player.data.hand[0][1][0] == player.data.hand[0][2][0] and player.data.hand[0][3][0] == player.data.hand[0][4][0]:
                                player2_card = player.data.hand[0][0][0]
                            else:
                                player2_card = player.data.hand[0][4][0]

                            if player1_card > player2_card:
                                players.remove(player)
                            elif player1_card == player2_card:
                                player_count += 1
                            else:
                                player_count = removes(players, player, player_count)
                        else:
                            players.remove(player)
                    else:
                        players.remove(player)

                # If both players have a one pair
                elif top_rank == 9:
                    player1_cards = [] 
                    player2_cards = []

                    if player.data.hand[0][0][0] == player.data.hand[0][1][0]:
                        player2_cards.append(player.data.hand[0][2][0])
                        player2_cards.append(player.data.hand[0][3][0])
                        player2_cards.append(player.data.hand[0][4][0])
                        player2_cards.append(player.data.hand[0][0][0])
                    elif player.data.hand[0][1][0] == player.data.hand[0][2][0]:
                        player2_cards.append(player.data.hand[0][0][0])
                        player2_cards.append(player.data.hand[0][3][0])
                        player2_cards.append(player.data.hand[0][4][0])
                        player2_cards.append(player.data.hand[0][1][0])
                    elif player.data.hand[0][2][0] == player.data.hand[0][3][0]:
                        player2_cards.append(player.data.hand[0][0][0])
                        player2_cards.append(player.data.hand[0][1][0])
                        player2_cards.append(player.data.hand[0][4][0])
                        player2_cards.append(player.data.hand[0][2][0])
                    else:
                        player2_cards.append(player.data.hand[0][0][0])
                        player2_cards.append(player.data.hand[0][1][0])
                        player2_cards.append(player.data.hand[0][2][0])
                        player2_cards.append(player.data.hand[0][3][0])

                    if player.prev.data.hand[0][0][0] == player.prev.data.hand[0][1][0]:
                        player1_cards.append(player.prev.data.hand[0][2][0])
                        player1_cards.append(player.prev.data.hand[0][3][0])
                        player1_cards.append(player.prev.data.hand[0][4][0])
                        player1_cards.append(player.prev.data.hand[0][0][0])
                    elif player.prev.data.hand[0][1][0] == player.prev.data.hand[0][2][0]:
                        player1_cards.append(player.prev.data.hand[0][0][0])
                        player1_cards.append(player.prev.data.hand[0][3][0])
                        player1_cards.append(player.prev.data.hand[0][4][0])
                        player1_cards.append(player.prev.data.hand[0][1][0])
                    elif player.prev.data.hand[0][2][0] == player.prev.data.hand[0][3][0]:
                        player1_cards.append(player.prev.data.hand[0][0][0])
                        player1_cards.append(player.prev.data.hand[0][1][0])
                        player1_cards.append(player.prev.data.hand[0][4][0])
                        player1_cards.append(player.prev.data.hand[0][2][0])
                    else:
                        player1_cards.append(player.prev.data.hand[0][0][0])
                        player1_cards.append(player.prev.data.hand[0][1][0])
                        player1_cards.append(player.prev.data.hand[0][2][0])
                        player1_cards.append(player.prev.data.hand[0][3][0])
                    
                    if player1_cards[3] > player2_cards[3]:
                        players.remove(player)
                    elif player1_cards[3] == player2_cards[3]:
                        if player1_cards[2] > player2_cards[2]:
                            players.remove(player)
                        elif player1_cards[2] == player2_cards[2]:
                            if player1_cards[1] > player2_cards[1]:
                                players.remove(player)
                            elif player1_cards[1] == player2_cards[1]:
                                if player1_cards[0] > player2_cards[0]:
                                    players.remove(player)
                                elif player1_cards[0] == player2_cards[0]:
                                    player_count += 1
                                else:
                                    player_count = removes(players, player, player_count)
                            else:
                                player_count = removes(players, player, player_count)
                        else:
                            player_count = removes(players, player, player_count)
                    else:
                        player_count = removes(players, player, player_count)

                # If both players have a high card
                else:
                    i = 4
                    while i > -1:
                        if player.data.hand[0][i][0] > player.prev.data.hand[0][i][0]:
                            player_count = removes(players, player, player_count)
                            i = -1
                        elif player.data.hand[0][i][0] < player.prev.data.hand[0][i][0]:
                            players.remove(player)
                            i = -1
                        else:
                            i -= 1
                    if player.data.hand[0][0][0] == player.prev.data.hand[0][0][0]:
                        player_count += 1
        
        # If the current players rank is higher (worse)
        else:
            players.remove(player)
        player = player.next
    
    # Pays out pot to all players tied for first
    pot.size = int(pot.size/player_count)
    head = players.head
    head.data.balance += pot.size
    head = head.next
    while head != players.head:
        head.data.balance += pot.size
    
    return

def removes(players, player, count):
    # Remove all players tied for first
    for _ in range(count):
        players.remove(player.prev)
    return 1

def preFlopBetting(players, player, table, BIG_BLIND):
    # While the players bet isn't the table's bet
    while player.data.current_bet != table.topBet:
        decision = checkBetFoldCall(player,table)
        if decision == 7:
            player = player.next
            preFlopBetting(players, player, table, BIG_BLIND)
        elif decision == 9:
            players.removePost(player)
            player = player.next
        else:
            player = player.next

    # Allow the BIG_BLIND to bet in the pre-flop round
    if player.data.current_bet == BIG_BLIND:
        decision = checkBetFoldCall(player,table)
        if decision == 7:
            player = player.next
            preFlopBetting(players, player, table, BIG_BLIND)
        elif decision == 9:
            players.removePost(player)
            player = player.next
        else:
            player = player.next

def postFlopBetting(players, player, table):
    # If the current table bet is 0
    if table.topBet == 0:
        # Allows checking through
        while player != players.head:
            # Allows bets
            decision = checkBetFoldCall(player, table)
            if decision == 7:
                player = player.next
                postFlopBetting(players, player, table)
                return
            elif decision == 9:
                players.removePost(player)
                player = player.next
            else:
                player = player.next
        # Lets dealer (head of LL) have a turn
        decision = checkBetFoldCall(player,table)
        if decision == 7:
            player = player.next
            postFlopBetting(players, player, table)
            return
        elif decision == 9:
            players.removePost(player)
            player = player.next
        else:
            player = player.next
    # If the current table bet is >0
    else:
        # Makes players match bet or fold
        while player.data.current_bet != table.topBet:
            decision = checkBetFoldCall(player,table)
            if decision == 7:
                player = player.next
                postFlopBetting(players, player, table)
                return
            elif decision == 9:
                players.removePost(player)
                player = player.next
            else:
                player = player.next
        return
    
def checkFolds(players, table):
    # If there is only one player left - they win
    player = players.head
    if player == player.next:
        player.data.balance += table.pot.size
        table.pot.size = 0
    return

def clearBets(players, table):
    # Add players bets to pot after each round of betting
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
    # Allows each player to have a turn
    bool = False
    while(not bool):
        try:
            # Prints out user specific information
            print("\nPLAYER ACTION REQUIRED")
            print(player.data.initialize())
            # Prints table state
            print(f"\nCards: {table.cards}")
            print(f"Top Bet: ${table.topBet}")
            # Allows player to make turn decision
            keyPress = int(input("1. Check\n2. Bet\n3. Call\n4. Fold\n"))
            match(keyPress):
                case 1:
                    # Check
                    if player.data.current_bet != table.topBet:
                        print("\nERROR: You can't check.")
                    else:
                        return 6
                case 2:
                    # Bet
                    bet_amount = int(input("How much would you like to bet? "))
                    if bet_amount > player.data.balance:
                        print("\nERROR: You can't bet that much")
                    elif bet_amount <= table.topBet - player.data.current_bet:
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

def deal_cards(LL, deck):
    # Deals 1 card to each player
    curr = LL.head
    curr.data.hand.append(deck.pop())
    curr = curr.next
    while curr != LL.head:
        curr.data.hand.append(deck.pop())
        curr = curr.next
    return

def add_card(table, deck):
    # Burn and Turn (append to table hand)
    deck.pop()
    table.cards.append(deck.pop())
    return


# Starting code of the interface
print("Welcome to Poker Simulator!")

# Allows user to start game, or run new round
bool = False
while(not bool):
    keyPress = input("To begin type 'Start' to quit type 'Quit'\n")
    match(keyPress):
        case "Start":
            new_round(create_game())
            break
        case "Quit":
            bool = True
            break
        case _:
            print("Invalid input") 