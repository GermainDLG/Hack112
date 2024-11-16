from cmu_graphics import *
from deck_class import Deck
from EV import calculateEV


class Bot:

    def __init__(self, hand, difficulty, deck, board):
        botRanges = {'Scared': (.48,.90) , 'Medium': (.33,.75), 'Aggressive': (.25, .38)}

        self.difficulty = difficulty
        self.hand = hand
        self.board = board
        self.range = botRanges[difficulty]
        self.bets = 0
    
    def makeMove(self, currBet, potSize, minBet, round): 
    #Given currBet(bet needed to stay in game) and potSize(size of pot in $$), return move as a string (check, bet, raise, bet {value})
        self.visible = readBoard(self.board, round)
        ev = calculateEV(self.hand, self.visible, potSize, self.bets+currBet)
        min, max = self.range
        if ev < min:
            if currBet != 0:
                return 'fold'
            else:
                return 'check'
        elif ev >= min and ev <= max:
            if currBet != 0:
                return 'call ' + str(currBet)
            else:
                return 'check'
        else:
            bet = currBet + minBet #+ evToBet(ev, potSize)
            self.bets += bet
            return 'raise ' + str(bet)
    
    def __repr__(self):
        return f'Bot: {self.difficulty}, Hand: {self.hand}'


def readBoard(board, round):
    if round == 0:
        return []
    else:
        return board[:(round+2)]


# potSize = 0
# minBet = 5
# players = []
# def playRound(minBet, potSize, players):
#     i = 0
#     currPlayer = 0
#     currBet = 0
#     while i < len(players):
#         player = players[currPlayer]
#         if isinstance(player, Bot):
#             move = player.makeMove(currBet, potSize, minBet) #will return move as a string
#             if move == 'fold':
#                 players.remove(player)
#                 i += 1
#                 continue
#             elif move == 'check':
#                 currPlayer += 1
#                 i += 1
#                 continue
#             elif move[:4] == 'call':
#                 potSize += int(move[6:])
#                 currPlayer += 1
#                 i += 1
#                 continue
#             elif move[:5] == 'raise':
#                 currBet = int(move[7:])
#                 potSize += currBet
#                 i = 0
#                 currPlayer += 1
#                 continue
#         else:
#             app.currBet = currBet
#             app.userTurn = True
#             app.userMove = None
#             while app.userMove == None:
#                 continue
#             move = app.userMove

#             if move == 'fold':
#                 players.remove(player)
#                 i += 1
#                 continue
#             elif move == 'check':
#                 currPlayer += 1
#                 i += 1
#                 continue
#             elif move[:4] == 'call':
#                 potSize += int(move[6:])
#                 currPlayer += 1
#                 i += 1
#                 continue
#             elif move[:5] == 'raise':
#                 currBet = int(move[7:])
#                 potSize += currBet
#                 i = 0
#                 currPlayer += 1
#                 continue





