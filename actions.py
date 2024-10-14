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

def blinds(players, small, big, pot):
    players[0].balance -= small
    players[0].current_bet = small
    print(f" {players[0].name} bets Small Blind: ${small}")
    players[1].balance -= big
    players[0].current_bet = big
    print(f" {players[1].name} bets Big Blind: ${big}")
    pot.size += (small + big)
    return

def fold(players, player):
    players = players.pop(player)
    return

def call(players, player, current_bet, top_bet, pot):
    pot.raise_pot(top_bet-current_bet)