#Solves zero sum games
#Player -1 wants minimum score, player 1 wants maximum

ENDGAME = 10000

myCache = {}
hits = 0
misses = 0
def TTTscore(state):
    global hits, misses
    str_state = str(state)
    if str_state in myCache:
        hits+=1
        return myCache[str_state]
    misses+=1
    wins = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    s = 0
    def same(i,j):
        return state[i]==state[j]
    def win(state):
        for w in wins:
            if state[w[0]]==state[w[1]]==state[w[2]]!=0: #Win
                   return state[w[0]]
        return False
    
    v = win(state)
    if v:
        myCache[str_state] = ENDGAME*v
        return ENDGAME*v
    
    for i in range(len(state)):
        if state[i]==0:
            state[i]=1
            if(win(state)):
                s+=1
            state[i]=-1
            if(win(state)):
                s-=1
            state[i]=0
    
#    myCache[str_state] = s
    return s

def TTTgetNext(player, state):
    result = []
    for i, place in enumerate(state):
        if place==0:
            state[i]=player
            result.append(state[:])
            state[i]=0
    return result

def TTTprintBoard(state):
    for i in range(len(state)):
        print "%3d" % state[i],
        if (i+1)%3==0:
            print
    print '-----------------------------------'


def minmax(player, state, max_level=7, level=0, tree=False, getNext = TTTgetNext, score = TTTscore):
    s = score(state)
    if abs(s)==ENDGAME: #Game over, stop!
        if tree:
            return (s, [], level)
        else:
            return (s,None, level)

    states = getNext(player, state)
    if states == []:
        if tree:
            return (s, [], level)
        else:
            return (s,None, level)

    needed_depth = max_level

    if level==max_level:
        best = states[0]
        bestScore = score(best)
        for nextState in states:
            curScore = score(nextState)
            if (player==1 and curScore>bestScore) or (player == -1 and curScore<bestScore):
                if tree:
                    best = [nextState]
                else:
                    best = nextState
                bestScore = curScore
    else:
        best = None
        for nextState in states:
            curScore, curBest, curDepth = minmax(-player,nextState, max_level, level+1, tree, getNext, score)
            if best==None or (player==-1 and curScore<bestScore) or (player==1 and curScore>bestScore) or (curScore==bestScore and curDepth<needed_depth):
                if tree:
                    best = curBest
                    best.append(nextState)
                else:
                    best = nextState
                bestScore = curScore
                needed_depth = curDepth
                if bestScore == player*ENDGAME: #No point in continuing to greater depth if victory is guaranteed, but keep checking for faster win
                    max_level = needed_depth
    if level==0 and tree:
        best.reverse()
    return bestScore,best, needed_depth

def play(getNext = TTTgetNext, score = TTTscore, printBoard = TTTprintBoard):
    state = [0]*9
    computer = -1
    player = 1
    while abs(score(state))!=ENDGAME and getNext(computer,state)!=[]:
        state = minmax(computer, state, 4, getNext=getNext, score=score)[1]
        printBoard(state)
        if abs(score(state))!=ENDGAME and getNext(player,state)!=[]:
            move = -1
            while not (0 <= move <=8 and state[move]==0):
                move = int(raw_input("Make a move\n"))
            state[move]=player
            printBoard(state)


minmax(1,[0]*9,9)
minmax(1,[0]*9,9)
minmax(1,[0]*9,9)

print hits,misses
