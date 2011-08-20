#Solves zero sum games
#Player -1 wants minimum score, player 1 wants maximum

ENDGAME = 10000


minmaxCache = {}
#Minmax cache keys are player,board
#The items are best score, next board, required depth
#Items only go into the cache if:
#  a)Guaranteed win/loss
#  b)Researched to max depth

minmaxHits = 0
minmaxMisses = 0

class Game:
    """Implements the functions needed to play a game"""
    

    def __init__(self):
        """"""

    def initialBoard(self):
        """Returns the game before any player has made a move"""
        
    def getCache(self):
        """Every game must define a cache like so:
        cache = { 'cache':{}, 'hits': 0, 'misses':0 }
        """

    def scoreCache(self, board):
        str_board = str(board)
        cache = self.getCache()
        if str_board in cache['cache']:
            cache['hits']+=1
            return cache['cache'][str_board]
        cache['misses']+=1
        result = self.score(board)
        cache['cache'][str_board] = result
        return result
    
    def score(self, board):
        """Returns a heuristic for the score of a game"""

    def getNext(self, player, board):
        """Returns list of possible next states"""

    def printBoard(self, board):
        """Prints a board in some user friendly way"""

class TicTacToe(Game):
    wins = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))

    cache = { 'cache':{}, 'hits': 0, 'misses':0 }
    #cache keys are boards.
    #The items are the score

    def initialBoard(self):
        return [0]*9

    def getCache(self):
        return TicTacToe.cache
    def win(self, board):
        for w in TicTacToe.wins:
            if board[w[0]]==board[w[1]]==board[w[2]]!=0:
                return board[w[0]]
        return False

    def score(self, board):
        winner = self.win(board)
        if winner:
            return ENDGAME*winner
        s = 0
        for i in range(9):
            if board[i]==0:
                board[i]=1
                if(self.win(board)):
                    s+=1
                board[i]=-1
                if(self.win(board)):
                    s-=1
                board[i]=0
        return s

    def getNext(self, player, board):
        result = []
        for i, place in enumerate(board):
            if place==0:
                board[i]=player
                result.append(board[:])
                board[i]=0
        return result

    def printBoard(self, board):
        for i in range(len(board)):
            print "%3d" % board[i],
            if (i+1)%3==0:
                print
        print '-----------------------------------'



'''def c4score(board):
    def win():
        #Column
        for i in xrange(7):
            for j in xrange(3):
                if 0 != board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3]:
                    return board[i][j]
        #Row
        for j in xrange(6):
            for i in xrange(4):
                if 0 != board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j]:
                    return board[i][j]

        #up right (bottom left)
        for i in xrange(4):
            for j in xrange(3):
                if 0 != board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3]:
                    return board[i][j]

        up left (bottom right):
        for i in xrange(3,7):
            for j in 
            
    for i in xrange(7):
        for i in xrange(6):
'''

def minmax(player, board, max_level=7, level=0, tree=False, game = TicTacToe()):
    global minmaxHits, minmaxMisses
    if (player, str(board)) in minmaxCache:
        minmaxHits+=1
        return minmaxCache[(player, str(board))]
    minmaxMisses+=1
    s = game.scoreCache(board)
    if abs(s)==ENDGAME: #Game over, stop!
        if tree:
            minmaxCache[(player, str(board))] = (s, [], level)
            return (s, [], level)
        else:
            minmaxCache[(player, str(board))] = (s, None, level)
            return (s,None, level)

    nextBoards = game.getNext(player, board)
    if nextBoards == []: #No more moves, stop!
        if tree:
            return (s, [], level)
        else:
            return (s,None, level)

    needed_depth = max_level

    if level==max_level:
        best = nextBoards[0]
        bestScore = game.scoreCache(best)
        for nextBoard in nextBoards:
            curScore = game.score(nextBoard)
            if (player==1 and curScore>bestScore) or (player == -1 and curScore<bestScore):
                if tree:
                    best = [nextBoard]
                else:
                    best = nextBoard
                bestScore = curScore
    else:
        best = None
        for nextBoard in nextBoards:
            curScore, curBest, curDepth = minmax(-player,nextBoard, max_level, level+1, tree, game)
            if best==None or (player==-1 and curScore<bestScore) or (player==1 and curScore>bestScore) or (curScore==bestScore and curDepth<needed_depth):
                if tree:
                    best = curBest
                    best.append(nextBoard)
                else:
                    best = nextBoard
                bestScore = curScore
                needed_depth = curDepth
                if bestScore == player*ENDGAME: #No point in continuing to greater depth if victory is guaranteed, but keep checking for faster win
                    max_level = needed_depth
    if level==0 and tree:
        best.reverse()
    if level==0 or abs(bestScore) == ENDGAME:
        minmaxCache[(player, str(board))] = bestScore, best, needed_depth 
    return bestScore,best, needed_depth

def playAgainst(game = TicTacToe()):
###
#TODO: Fix this to work with game objects
###
    board = game.initialBoard()
    computer = -1
    player = 1
    while abs(game.scoreCache(board))!=ENDGAME and game.getNext(computer,board)!=[]:
        board = minmax(computer, board, 7, game = game)[1]
        game.printBoard(board)
        if abs(game.scoreCache(board))!=ENDGAME and game.getNext(player,board)!=[]:
            ###TODO:###
            ###General board input function
            ###
            move = -1
            while not (0 <= move <=8 and board[move]==0):
                move = int(raw_input("Make a move\n"))
            board[move]=player
            game.printBoard(board)

def play(game = TicTacToe()):
###
#TODO: Fix this to work with game objects
###
    p1 = -1
    p2 =  1
    board = game.initialBoard()
    game.printBoard(board)
    while abs(game.score(board))!=ENDGAME and game.getNext(p1,board)!=[]:
        board = minmax(p1, board, 7, game = game)[1]
        game.printBoard(board)
        if abs(game.score(board))!=ENDGAME and game.getNext(p2,board)!=[]:
            board = minmax(p2, board, 7, game = game)[1]
            game.printBoard(board)
