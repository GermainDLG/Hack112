from cmu_graphics import *
from deck_class import Deck
import time
from NPCs import Bot
from NPCs import readBoard

def main():
    runApp()

def onAppStart(app):
    app.width = 800
    app.height = 800
    app.deck = Deck()
    app.deck.generateDeck()
    app.deck.delegateCards()
    app.turn = 0
    app.userTurn = False
    app.currBet = 0
    app.round = 0

    app.board = app.deck.flop + [app.deck.river] + [app.deck.turn]

    app.bot1 = Bot(app.deck.hand2, 'Scared', app.deck, app.board)
    app.bot2 = Bot(app.deck.hand3, 'Medium', app.deck, app.board)
    app.bot3 = Bot(app.deck.hand4, 'Aggressive', app.deck, app.board)

    print(app.deck)
    print(app.board)
    print(app.bot1)
    print(app.bot2)
    print(app.bot3)

    app.minBet = 10
    app.potSize = 0
    app.players = ['user', app.bot1, app.bot2, app.bot3]

def restart(app):
    app.deck = Deck()
    app.deck.generateDeck()
    app.deck.delegateCards()
    app.turn = 0

def redrawAll(app):
    drawBoard(app)
    drawCards(app)
    drawRest(app)

def drawBoard(app):
    #Draws board
    drawRect(0, 0, app.width, app.height, fill='brown')
    drawRect(50,50, app.width-100,app.height-100,fill='green')
    for x,y in [(50,50), (50,app.height-50), (app.width-50,app.height-50), (app.width-50,50)]:
        drawCircle(x,y,50,fill='brown')
    #Draws NPC Cards
    drawRect(25,300,150,100,fill='black')
    drawRect(25,410,150,100,fill='black')
    drawRect(625,300,150,100,fill='black')
    drawRect(625,410,150,100,fill='black')
    drawRect(295,25,100,150,fill='black')
    drawRect(405,25,100,150,fill='black')
    #Draws Log
    drawRect(515,20,250,175, border='black', fill='white')
    #Draws Buttons
    drawRect(515, 570, 250, 225, fill='white', border='black')
    buttonWidth, buttonHeight = 205/2, 180/2
    drawRect(530, 585, buttonWidth, buttonHeight, border='black', fill='white')
    drawLabel(f'Check/Fold', 530 + buttonWidth/2, 585 + buttonHeight/2, size=15, bold=True)
    drawRect(530 + buttonWidth + 15, 585 + buttonHeight + 15, buttonWidth, buttonHeight, border='black', fill='white')
    drawLabel(f'Raise  {app.currBet}', 545 + buttonWidth + buttonWidth/2, 600 + buttonHeight + buttonHeight/2, size=15, bold=True)
    drawRect(530 + buttonWidth + 15, 585, buttonWidth, buttonHeight, border='black', fill='white')
    drawLabel(f'Call  {app.currBet}', 545 + buttonWidth + buttonWidth/2, 585 + buttonHeight/2, size=15, bold=True)
    #drawRect(530, 585 + buttonHeight + 15, buttonWidth, buttonHeight, border='black', fill='white')

def drawCards(app):
    #Draws player cards
    drawRect(295,625,100,150,fill='white')
    drawRect(405,625,100,150,fill='white')
    if(app.deck.hand1[0][-1] == 'D' or app.deck.hand1[0][-1] == 'H'):
        drawLabel(app.deck.hand1[0],345,700,fill='red')
    else:
        drawLabel(app.deck.hand1[0],345,700)
    if(app.deck.hand1[1][-1] == 'D' or app.deck.hand1[1][-1] == 'H'):
        drawLabel(app.deck.hand1[1],455,700,fill='red')
    else:
        drawLabel(app.deck.hand1[1],455,700)

def drawRest(app):
    #Draws flop, turn, river
    drawRect(225,225,100,150,fill='white')
    if(app.deck.flop[0][-1] == 'D' or app.deck.flop[0][-1] == 'H'):
        drawLabel(app.deck.flop[0],275,300,fill='red')
    else:
        drawLabel(app.deck.flop[0],275,300)
    drawRect(350,225,100,150,fill='white')
    if(app.deck.flop[1][-1] == 'D' or app.deck.flop[1][-1] == 'H'):
        drawLabel(app.deck.flop[1],400,300,fill='red')
    else:
        drawLabel(app.deck.flop[1],400,300)
    drawRect(475,225,100,150,fill='white')
    if(app.deck.flop[2][-1] == 'D' or app.deck.flop[2][-1] == 'H'):
        drawLabel(app.deck.flop[2],525,300,fill='red')
    else:
        drawLabel(app.deck.flop[2],525,300)
    if(app.turn >= 1):
        drawRect(275,400,100,150,fill='white')
        if(app.deck.turn[-1] == 'D' or app.deck.turn[-1] == 'H'):
            drawLabel(app.deck.turn,325,475,fill='red')
        else:
            drawLabel(app.deck.turn,325,475)
    if(app.turn >= 2):
        drawRect(425,400,100,150,fill='white')
        if(app.deck.river[-1] == 'D' or app.deck.river[-1] == 'H'):
            drawLabel(app.deck.river,475,475,fill='red')
        else:
            drawLabel(app.deck.river,475,475)

def onKeyPress(app,key):
    if(key=='space'):
        if(app.turn < 2):
            app.turn += 1
            time.sleep(2)
            print('hello')
            time.sleep(2)
            print('hello')
        else:
            restart(app)

def onMousePress(app, mouseX, mouseY): #call, check, fold, raise
    if app.userTurn:
        if(inCallButton(mouseX, mouseY) == True):
            app.userMove = f'call {app.currBet}'
        elif(inCheckButton(mouseX, mouseY) == True):
            if app.currBet != 0:
                app.userMove = 'fold'
            else:
                app.userMove = 'check'
        elif(inRaiseButton(mouseX, mouseY) == True):
            app.userMove = f'raise {app.currBet}'

def inCallButton(mouseX, mouseY):
    buttonWidth, buttonHeight = 205/2, 180/2
    left, top = 530 + buttonWidth + 15, 585
    right, bottom = left + buttonWidth, top + buttonHeight
    return (left <= mouseX <= right) and (top <= mouseY <= bottom)

def inCheckButton(mouseX, mouseY):
    buttonWidth, buttonHeight = 205/2, 180/2
    left, top = 530, 585
    right, bottom = left + buttonWidth, top + buttonHeight
    return (left <= mouseX <= right) and (top <= mouseY <= bottom)

def inRaiseButton(mouseX, mouseY):
    buttonWidth, buttonHeight = 205/2, 180/2
    left, top = 530 + buttonWidth + 15, 585 + buttonHeight + 15
    right, bottom = left + buttonWidth, top + buttonHeight
    return (left <= mouseX <= right) and (top <= mouseY <= bottom)

def playRound(app, minBet, potSize, players):
    i = 0
    currPlayer = 0
    currBet = 0
    while i < len(players):
        player = players[currPlayer]
        if isinstance(player, Bot):
            move = player.makeMove(currBet, potSize, minBet) #will return move as a string
            if move == 'fold':
                players.remove(player)
                i += 1
                print(player, move)
                continue
            elif move == 'check':
                currPlayer += 1
                i += 1
                print(player, move)
                continue
            elif move[:4] == 'call':
                potSize += int(move[6:])
                currPlayer += 1
                i += 1
                print(player, move)
                continue
            elif move[:5] == 'raise':
                currBet = int(move[7:])
                potSize += currBet
                i = 0
                currPlayer += 1
                print(player, move)
                continue
        else:
            app.currBet = currBet
            app.userTurn = True
            app.userMove = None
            while app.userMove == None:
                continue
            move = app.userMove

            if move == 'fold':
                players.remove(player)
                i += 1
                print(player, move)
                continue
            elif move == 'check':
                currPlayer += 1
                i += 1
                print(player, move)
                continue
            elif move[:4] == 'call':
                potSize += int(move[6:])
                currPlayer += 1
                i += 1
                print(player, move)
                continue
            elif move[:5] == 'raise':
                currBet = int(move[7:])
                potSize += currBet
                i = 0
                currPlayer += 1
                print(player, move)
                continue

main()
 