import random
import rankHand as rankHand
import createDeck as createDeck
import decodeHand as decodeHand

def best_hand(cards_in_play):

    # Any empty list that will be used to find the best hand possible
    possibleHands = []

    # This removes one card from the 7 possible
    for i in range(len(cards_in_play)-1):
        removeOne = cards_in_play[:]
        removeOne.pop(i)

        # This removes the second card so there are only ever 5 cards being played
        for j in range(i, len(removeOne)):
            removeTwo = removeOne[:]
            removeTwo.pop(j)
            # Gives each hand a rank so they can be sorted later
            removeTwo.append(rank(removeTwo))
            possibleHands.append(removeTwo)

    # Sorts the hands by the rank - which is assigned as the last index (highest rank reported first)
    possibleHands.sort(key=lambda x: int(x[-1]))
    return possibleHands
        
# Tests shuffling and sorting functions
def rank(hand):
    if rankHand.royalFlush(hand):
        return 1
    elif rankHand.straightFlush(hand):
        return 2
    elif rankHand.fourKind(hand):
        return 3
    elif rankHand.fullHouse(hand):
        return 4
    elif rankHand.flush(hand):
        return 5
    elif rankHand.straight(hand):
        return 6
    elif rankHand.threeKind(hand):
        return 7
    elif rankHand.twoPair(hand):
        return 8
    elif rankHand.onePair(hand):
        return 9
    else:
        return 10
    

# Random cards a player is dealt
deck = createDeck.createDeck()
random.shuffle(deck)
hands = deck[0:7]
hands = decodeHand.decode(hands)

print("\n", hands, "\n")

for i in range(len(best_hand(hands))):
    print(best_hand(hands)[i])


