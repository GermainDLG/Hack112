def calculateEV(hand, seen, pot, bet):
    odds = {'high card': .174, 'one pair': .499, "two pair": .652, "three of a kind": .732, "straight": .844, "flush": .915, "full house": .978, "quads": .992, "straight flush": .999, "royal flush": 1}
    hand = getHand(hand, seen)
    winPer = odds[hand]
    losePer = 1 - winPer
    return ((winPer * pot) - (losePer * bet)) / pot

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
            value = 1
            values.append(value)
            continue
        else:
            value = card[0]
        values.append(value)
    
    
    for suit in suits:
        if suits[suit] >= 5:
            flush = True
        else:
            flush = False

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
    
    
