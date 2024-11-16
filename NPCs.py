from cmu_graphics import *
import Deck

class Bot:

    def __init__(self, hand, difficulty):
        botRanges = {'Easy': () , 'Medium': (), 'Hard': ()}

        self.difficulty = difficulty
        self.hand = hand
        self.board = readDeck()
        self.range = botRanges[self.difficulty]
        self.bets = 0
    
    def makeMove(self, currBet, potSize, minBet): 
    #Given currBet(bet needed to stay in game) and potSize(size of pot in $$), return move as a string (check, bet, raise, bet {value})
        ev = calculateEV(self.hand, self.board, potSize, self.bets)
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

# class Player:

#     def __init__(self, hand):
#         self.hand = hand
#         self.view = readTable()

# def readDeck(deck):
#     return deck.visible


# potSize = 0
# minBet = 
# def playRound(minBet, potSize, )
#     i = 0
#     currPlayer = 0
#     currBet = 0
#     players = [bot1, bot2, bot3, manual]
#     while i < len(players):
#         player = players[i]
#         move = player.makeMove() #will return move as a string
#         if move == 'fold':
#             players.remove(player)
#             i += 1
#             continue
#         elif move == 'check':
#             currPlayer += 1
#             i += 1
#             continue
#         elif move[:4] == 'call':
#             potSize += move[6:]
#             currPlayer += 1
#             i += 1
#             continue
#         elif move[:5] == 'raise':
#             currBet = move[7:]
#             potSize += 



