# Rank 1
def royalFlush(hand):
    return straightFlush(hand) and hand[0][0] == 10

# Rank 2
def straightFlush(hand):
    return straight(hand) and flush(hand)

# Rank 3
def fourKind(hand):
    return hand[0][0] == hand[1][0] == hand[2][0] == hand[3][0] or hand[1][0] == hand[2][0] == hand[3][0] == hand[4][0]

# Rank 4
def fullHouse(hand):
    return (threeKind(hand=hand[0:3]) and onePair(hand=hand[3:5])) or  (onePair(hand=hand[0:2]) and threeKind(hand=hand[2:5]))

# Rank 5
def flush(hand):
    for i in range(len(hand)-1):
        if hand[i][-1] != hand[i+1][-1]:
            return False
    return True

# Rank 6
def straight(hand):
    if hand[-1][0] == 14 and hand[-2][0] != 14 and hand[-2][0] != 13 and hand[0][0] == 2:
        new_hand = hand[:]
        new_hand[-1][0] = 1
        new_hand.sort(key=lambda x: x[0])
        return straight(new_hand)
    else:
        for i in range(len(hand)-1):
            if hand[i][0] + 1 != hand[i+1][0]:
                return False
        return True

# Rank 7
def threeKind(hand):
    for i in range(len(hand)-2):
        if hand[i][0] == hand[i+1][0] == hand[i+2][0]:
            return True
    return False

# Rank 8
def twoPair(hand):
    #Case 1 = [0,0,1,2,2]

    if onePair(hand=hand[0:2]) and onePair(hand=hand[3:5]):
        return True

    #Case 2 = [0,1,1,2,2]
    elif onePair(hand=hand[1:3]) and onePair(hand=hand[3:5]):
        return True
    
    #Case 3 = [0,0,1,1,2]
    elif onePair(hand=hand[0:2]) and onePair(hand=hand[2:4]):
        return True
    
    else:
        return False

# Rank 9
def onePair(hand):
    for i in range(len(hand)-1):
        if hand[i][0] == hand[i+1][0]:
            return True
    return False

# Rank 10
def highCard(hand):
    return True
