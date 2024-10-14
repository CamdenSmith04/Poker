def decode(hand):
    numericalHand = []
    for i in range(len(hand)):
        if len(hand[i]) == 3:
            numericalHand.append([hand[i][0:2],hand[i][-1]])
        else:
            numericalHand.append([hand[i][0],hand[i][-1]])

    
    return numerical(numericalHand)

def numerical(hand):
    to_Numbers = {"A" : 14,
                  "K" : 13,
                  "Q" : 12,
                  "J" : 11}
    for i in range(len(hand)):
        if hand[i][0] in to_Numbers:
            hand[i][0] = to_Numbers.get(hand[i][0])
        else:
            hand[i][0] = int(hand[i][0])
    hand.sort(key=lambda x: x[0])
    return hand
