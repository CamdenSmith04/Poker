def createDeck():
    deck = []

    suits = ["\u2663", "\u2665", "\u2666", "\u2660"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    for i in range(len(suits)):
        for j in range(len(ranks)):
            deck.append(ranks[j] + suits[i])

    return deck




