mapping = { 'royal flush': 10, 'straight flush': 9, 'four of a kind': 8, 'full house': 7, 'flush': 6,
            'straight': 5, 'three of a kind': 4, 'two pair': 3, 'one pair': 2, 'high card': 1,
            'A': 14, 'K': 13, 'Q': 12, 'J': 11 }

class card:
    def __init__(self, str):
        self.s = str[-1]
        self.r = mapping[str[:-1]] if str[:-1] in mapping else int(str[:-1])

    def __str__(self):
        r = self.r
        for (x, y) in mapping.items():
            r = x if self.r == y and r > 10 else r
        return str(r) + self.s

    def __lt__(self, other):
        return self.r < other.r

def isCard(str):
    SUITS = set(['S', 'C', 'D', 'H'])
    suit = str[-1]
    rank = mapping[str[:-1]] if str[:-1] in mapping else (int(str[:-1]) if str[:-1].isdigit() else 0)
    if (suit not in SUITS) or (1 > rank > 15):
        return False
    return True

def isEq(h1, h2):
    for x, y in zip(h1, h2):
        if x.r != y.r:
            return False
    return True

# Royal Flush
def is10(h):
    suit = h[0].s
    for i in range(5):
        if (h[i].r != 14 - i) or (h[i].s != suit):
            return is9(h)
    return 10, h

# Straight Flush
def is9(h):
    suit = h[0].s
    rank = h[0].r
    for i in range(5):
        if (h[i].r != rank - i) or (h[i].s != suit):
            return is8(h)
    return 9, h

# Four of a Kind
def is8(h):
    hi = h[0].r
    lo = h[4].r
    nHi = 0
    nLo = 0
    for c in h:
        if c.r == hi: nHi += 1
        elif c.r == lo: nLo += 1

    if (nHi != 4) and (nLo != 4):
        return is7(h)
    elif nHi == 4:
        return 8, h
    l = [h[i] for i in range(1,5)]
    l.append(h[0])
    return 8, l

# Full House
def is7(h):
    hi = h[0].r
    lo = h[4].r
    nHi = 0
    nLo = 0
    for c in h:
        if c.r == hi: nHi += 1
        elif c.r == lo: nLo += 1
    if (nHi == 3) and (nLo == 2):
        return 7, h
    elif (nHi == 2) and (nLo == 3):
        l = [h[i] for i in range(2,5)]
        l.append([h[i] for i in range(2)])
        return 7, l
    return is6(h)

# Flush
def is6(h):
    suit = h[0].s
    for c in h:
        if c.s != suit:
            return is5(h)
    return 6, h

# Straight
def is5(h):
    rank = h[0].r
    for i in range(5):
        if h[i].r != rank - i:
            return is4(h)
    return 5, h

# Three of a Kind
def is4(h):
    for i in range(5):
        count = 0
        for j in range(5):
            if h[i].r == h[j].r:
                count += 1
        if count == 3:
            l = [h[k] for k in range(i, i + 3)]
            for k in range(5):
                if (i + 2 < k) or (i > k):
                    l.append(h[k])
            return 4, l
    return is3(h)

# Two Pair
def is3(h):
    index = -1
    for i in range(5):
        count = 0
        for j in range(5):
            if h[i].r == h[j].r:
                count += 1
        if (count != 2) and (index != -1):
            return is2(h)
        elif count != 2:
            index = i
    l = [h[i] for i in range(5) if i != index]
    l.append(h[index])
    return 3, l

# One Pair
def is2(h):
    for i in range(5):
        count = 0
        for j in range(5):
            if h[i].r == h[j].r:
                count += 1
        if count == 2:
            l = [h[k] for k in range(i, i + 2)]
            for k in range(5):
                if (i + 1 < k) or (i > k):
                    l.append(h[k])
            return 2, l
    return is1(h)

# High Card
def is1(h):
    return 1, h

# A-2-3-4-5 Straight Flush or Straight:
def isStraight(h):
    if (h[0].r == 14) and (h[1].r == 5) and (h[2].r == 4) and (h[3] == 3) and (h[4] == 2):
        l = [h[i] for i in range(1, 5)]
        l.append(h[0])
        suit = h[0].s
        for c in h:
            if c.s != suit:
                return 5, l
        print(printHand(l))
        return 9, l
    return 0, h

def checkDuplicate(hands):
    s = set()
    for h in hands:
        for c in h:
            if str(c) in s:
                return True, printHand(h)
            s.add(str(c))
    return False, ''

def sameHand(h1, h2):
    for i in range(5):
        if(h1[i].r != h2[i].r):
            return False
    return True

def printHand(h):
    return '[' + str(h[0]) + ' ' + str(h[1]) + ' ' + str(h[2]) + ' ' + str(h[3]) + ' ' + str(h[4]) + ']'

def computeScore(h, hand):
    return h * 13 ** 5 + hand[0].r * 13 ** 4 + hand[1].r * 13 ** 3 + hand[2].r * 13 ** 2 + hand[3].r * 13 + hand[4].r