def calculateEV(hand, seen, pot, bet):
    if board == []:
        preflop = {"face cards":.8 , "connectors":.5, "suited":.5, "pair":.8, "suited connectors":.7, "nothing":.3, "one face":.4}
        hand = getPreflopHand(hand)
        ev = preflop[hand]
        return ev
    else:
        odds = {'high card': .174, 'one pair': .499, "two pair": .652, "three of a kind": .732, "straight": .844, "flush": .915, "full house": .978, "quads": .992, "straight flush": .999, "royal flush": 1}
        hand = getHand(hand, seen)
        winPer = odds[hand]
        losePer = 1 - winPer
        return ((winPer * pot) - (losePer * bet)) / pot


def getPreflopHand(hand):
    lst = []
    for card in hand:
        card = card.split(" ")
        suit = card[1]
        if card[0] == "J":
            value = 11
        elif card[0] == "Q":
            value = 12
        elif card[0] == "K":
            value = 13
        elif card[0] == "A":
            value = 14
        else:
            value = card[0]
        lst.append([int(value), suit])
    
    if lst[0][0] == lst[1][0]:
        pair = True
    else: pair = False
    
    if lst[0][0] >= 10 and lst[1][0] >= 10:
        faceCard = True
    else: faceCard = False
    
    if lst[0][0] > 10 or lst[1][0] > 10:
        oneFaceCard = True
    else: oneFaceCard = False
    
    if lst[0][1] == lst[1][1]:
        suited = True
    else: suited = False
    
    if abs(lst[0][0] - lst[1][0]) == 1:
        connectors = True
    else: connectors = False
       
       
    if pair:
        return "pair"
    elif faceCard:
        return "face cards"
    elif suited and connectors:
        return "suited connectors"
    elif suited: 
        return "suited"
    elif connectors:
        return "connectors"
    elif oneFaceCard:
        return "one face"
    else:
        return "nothing"


def getHand(hand, seen):
    suits = {'H': 0, 'D': 0, 'C': 0, 'S': 0}
    values = []
    for card in hand + seen:
        card = card.split(" ")
        suit = card[1]
        suits[suit] += 1
        if card[0] == "J":
            value = 11
        elif card[0] == "Q":
            value = 12
        elif card[0] == "K":
            value = 13
        elif card[0] == "A":
            value = 14
            values.append(value)
            continue
        else:
            value = int(card[0])
        values.append(value)
    
    for suit in suits:
        if suits[suit] >= 5:
            flush = True
        if isStraight(values):
            straight = True
        else:
            straight = False

    if straightFlush(hand+seen):
        if royal(values):
                return "royal flush"
        else:
                return "straight flush"
    elif flush:
        return "flush"
    elif straight:
        return "straight"

    if isQuads(values):
        return "quads"

    if isFullHouse(values):
        return "full house"

    if trips(values):
        return "three of a kind"
        
    if twoPair(values):
        return "two pair"

    if onePair(values):
        return "one pair"
            
    return "high card"

def onePair(values):
    if len(set(values)) == len(values) - 1:
        return True

def twoPair(values):
    d = {}
    count = 0
    for x in values:
        d[x] = d.get(x, 0) + 1
    for x in d:
        if d[x] == 2:
            count += 1
        elif d[x] > 2:
            return False
    if count == 2: return True
    else: return False

def trips(values):
    d = {}
    count = 0
    for x in values:
        d[x] = d.get(x, 0) + 1
    for x in d:
        if d[x] == 3:
            count += 1
        elif d[x] == 2:
            return False
        elif d[x] >3:
            return False
    if count == 1:
        return True
    else:
        return False

def isFullHouse(values):
    d = {}
    count3 = 0
    count2 = 0
    for x in values:
        d[x] = d.get(x, 0) + 1
    for x in d:
        if d[x] == 3:
            count3 +=1
        elif d[x] == 2:
            count2 += 1
    if count2 == 1 and count3 == 1:
        return True
    else: return False

def isQuads(values):
    d = {}
    count = 0
    for x in values:
        d[x] = d.get(x, 0) + 1
    for x in d:
        if d[x] == 4:
            return True
    return False

def isStraight(values):
    values = [int(x) for x in values]
    values = set(values)
    if 14 in values:
        values.add(1)
    values = sorted(values)
    max = len(values)
    for i in range(max):
        num = values[i]
        if values[i:i+5] == list(range(num,num+5)):
            return True
    return False
    

def straightFlush(cards):
    lst = []
    bestSuit = None
    suits = {'H': 0, 'D': 0, 'C': 0, 'S': 0}
    for card in cards:
        card = card.split(" ")
        suit = card[1]
        suits[suit] += 1
    for suit in suits:
        if suits[suit] >= 5:
            bestSuit = suit
    if bestSuit == None:
        return False
    for card in cards:
        card = card.split(" ")
        if card[0] == "J":
            value = 11
        elif card[0] == "Q":
            value = 12
        elif card[0] == "K":
            value = 13
        elif card[0] == "A":
            value = 14
        else:
            value = card[0]
        suit = card[1]
        
        if suit == bestSuit:
            lst.append(value)
        if isStraight(lst):
            return True
    return False


def royal(values):
    values = [int(x) for x in values]
    values = set(values)
    values = sorted(values)
    straight = values[-5:]
    if isStraight(straight) and straight[-1] == 14:
        return True
    else: return False
    
    

    
def winner(hands, board):
    d = {}
    scores = {}
    for hand1 in hands:
        hand = (hand1[0], hand1[1])
        d[hand] = getHand(list(hand), board)
        if d[hand] == "royal flush":
            scores[hand] = 270 + tiebreaker(bestHand(hand1, board))
        elif d[hand] == "straight flush":
            scores[hand] = 240 + tiebreaker(bestHand(hand1, board))
        elif d[hand] == "quads":
            scores[hand] = 210 + tiebreaker(bestHand(hand1, board))
        elif d[hand] == "full house":
            scores[hand] = 180 + tiebreaker(bestHand(hand1, board))
        elif d[hand] == "flush":
            scores[hand] = 150 + tiebreaker(bestHand(hand1, board))
        elif d[hand] == "straight":
            scores[hand] = 120 + tiebreaker(bestHand(hand1, board))
        elif d[hand] == "three of a kind":
            scores[hand] = 90 + tiebreaker(bestHand(hand1, board))
        elif d[hand] == "two pair":
            scores[hand] = 60 + tiebreaker(bestHand(hand1, board))
        elif d[hand] == "one pair":
            scores[hand] = 30 + tiebreaker(bestHand(hand1, board))
        elif d[hand] == "high card":
            scores[hand] = 0 + tiebreaker(bestHand(hand1, board))
    best = 0
    winningHands = set()
    for hand in scores:
        if scores[hand] > best:
            winningHands = {hand}
            best = scores[hand]
        elif scores[hand] == best:
            winningHands.add(hand)
    return winningHands
    
            
def bestHand(hand, board):
    cards = []
    suits = {'H': 0, 'D': 0, 'C': 0, 'S': 0}
    values = {2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0}
    typeHand = getHand(hand, board)
    for card in hand + board:
        card = card.split(" ")
        suit = card[1]
        suits[suit] += 1
        if card[0] == "J":
            value = 11
        elif card[0] == "Q":
            value = 12
        elif card[0] == "K":
            value = 13
        elif card[0] == "A":
            value = 14
        else:
            value = int(card[0])
        values[value] += 1
        cards.append((value, suit))
    cards = sorted(cards)
    newCards = []
    if typeHand == "straight flush" or typeHand == "flush":
        for hand in cards:
            value, suit = hand
            if suits[suit] >= 5:
                newCards.append(hand)
        return newCards
    if typeHand == "high card":
        return cards[-5:]
    if typeHand == "one pair":
        for hand in cards:
            value, suit = hand
            if values[value] == 2:
                newCards.append(hand)
        while len(newCards) != 5:
            if cards[-1] not in newCards:
                newCards.append(cards[-1])
            else: cards.pop()
        return list(reversed(newCards))
    if typeHand == "two pair":
        for hand in cards:
            value, suit = hand
            if values[value] == 2:
                newCards.append(hand)
        while len(newCards) != 5:
            if cards[-1] not in newCards:
                newCards.append(cards[-1])
            else: cards.pop()
        return list(reversed(newCards))
    if typeHand == "full house":
        for hand in cards:
            value, suit = hand
            if values[value] >= 2:
                newCards.append(hand)
        return list(reversed(newCards))
    if typeHand == "three of a kind":
        for hand in cards:
            value, suit = hand
            if values[value] == 3:
                newCards.append(hand)
        while len(newCards) != 5:
            if cards[-1] not in newCards:
                newCards.append(cards[-1])
            else: cards.pop()
        return list(reversed(newCards))
    if typeHand == "quads":
        for hand in cards:
            value, suit = hand
            if values[value] == 4:
                newCards.append(hand)
        while len(newCards) != 5:
            if cards[-1] not in newCards:
                newCards.append(cards[-1])
            else: cards.pop()
        return list(reversed(newCards))
    if typeHand == "straight":
        nums = []
        for card in hand + board:
            card = card.split(" ")
            suit = card[1]
            suits[suit] += 1
            if card[0] == "J":
                value = 11
            elif card[0] == "Q":
                value = 12
            elif card[0] == "K":
                value = 13
            elif card[0] == "A":
                value = 14
            else:
                value = int(card[0])
            nums.append(value)
        nums = sorted(nums)
        while len(cards) >= 5:
            seen = hand+board
            if isStraight(nums[-5:]):
                return cards[-5:]
            else:
                cards.pop()
            
        
        
def tiebreaker(hand):
    accHand = []
    for card in hand:
        value, suit = card
        accHand.append(f"{value} {suit}")
    typeHand = getHand(accHand, [])
    if typeHand == "straight" or typeHand == "straight flush" or typeHand == "quads":
        card = hand[-1]
        value, suit = card
        return value
    elif typeHand == "flush":
        card = hand[-1]
        value1, suit1 = card
        card = hand[-2]
        value2, suit2 = card
        return value1 + value2
    elif typeHand == "three of a kind":
        card = hand[-1]
        value1, suit1 = card
        card = hand[-4]
        value2, suit2 = card
        return value1 + value2
    elif typeHand == "one pair":
        card = hand[-1]
        value1, suit1 = card
        card = hand[-3]
        value2, suit2 = card
        return value1 + value2
    elif typeHand == "high card":
        card = hand[-1]
        value1, suit1 = card
        card = hand[-2]
        value2, suit2 = card
        return value1 + value2
    elif typeHand == "two pair":
        card = hand[-1]
        value1, suit1 = card
        card = hand[-3]
        value2, suit2 = card
        return value1 + value2
    elif typeHand == "full house":
        card = hand[-1]
        value1, suit1 = card
        card = hand[-4]
        value2, suit2 = card
        return value1 + value2
        
        
        
        
        
    

        