from player import Player
from pot import Pot

def deposit_funds(player, amount):
    player = player
    player.set_balance(player.balance + amount)
    return f"{player.name} deposits ${amount}"

def withdraw_funds(player, amount):
    player = player
    player.set_balance(player.balance - amount)
    return f"{player.name} withdraws ${amount}"

def bet(player, amount, pot):
    player = player
    pot.raise_pot(amount)
    player.set_balance(player.balance - amount)
    return f"{player.name} bets ${amount}"

def blinds(playersLL, small, big, pot):
    curr = playersLL.head
    curr.data.balance -= small
    curr.data.current_bet = small
    print(f"{curr.data.name} bets Blind: ${small}")
    curr = curr.next
    curr.data.balance -= big
    curr.data.current_bet = big
    print(f"{curr.data.name} bets Blind: ${big}")
    return

def fold(players, player):
    players = players.pop(player)
    return

def call(players, player, current_bet, top_bet, pot):
    pot.raise_pot(top_bet-current_bet)