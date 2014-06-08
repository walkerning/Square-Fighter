#!/us/bin/env python
# -*- coding: utf-8 -*-
# 数据结构，类定义
import copy

# --------- some help functions for all ------------

def printNotDefined():
    import traceback
    inspect = traceback.extract_stack()
    print "Method not implemented: %s"%inspect[-2][2]

def printAgentError(agent):
    print "%s seems not to be a legal agent with the getAction method!Default agent used."%agent

def printIllegalMove():
    print "Your placement is illegal"

def manhattanDistance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
# --------------------------------------------------

# -------- global parameters and data --------------
PILE_NUMBER = 21
SIZE = 14
NeighborVectors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
CrossVectors = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
PileSquareNumberList = (
1, 2, 3, 3, 4, 4, 4,
 4, 4, 5, 5, 5, 5, 5,
 5, 5, 5, 5, 5, 5, 5)

PileMaxManhattanList = (0, 1, 2, 2, 2, 2, 3, 3, 3, 3, 2, 3, 4, 4, 3, 4, 3, 3, 4, 4, 4)

PileRotateList =(
[[(0, 0)]],#0
[[(0, 0), (1, 0)], [(0, 0), (0, 1)]],#1
[[(0, 0), (0, 1), (1, 0)], [(0, 0), (1, 0), (1, 1)], [(0, 0), (1, -1), (1, 0)],[(0, 0), (0, 1), (1, 1)]],#2
[[(0, 0), (0, 1), (0, 2)], [(0, 0), (1, 0), (2, 0)]],#3
[[(0, 0), (0, 1), (0, 2), (1, 1)], [(0, 0), (1, -1), (1, 0), (1, 1)], [(0, 0), (1, -1), (1, 0), (2, 0)], [(0, 0), (1, 0), (1, 1), (2, 0)]],#4
[[(0, 0), (0, 1), (1, 0), (1, 1)]],#5
[[(0, 0), (0, 1), (0, 2), (1, 0)], [(0, 0), (1, 0), (1, 1), (1, 2)], [(0, 0), (1, -2), (1, -1), (1, 0)], [(0, 0), (0, 1), (0, 2), (1, 2)], [(0, 0), (1, 0), (2,-1), (2, 0)], [(0, 0), (0, 1), (1, 1), (2, 1)], [(0, 0), (0, 1), (1, 0), (2, 0)], [(0, 0), (1, 0), (2, 0), (2, 1)]],#6
[[(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 0), (1, 0), (2, 0), (3, 0)]],#7
[[(0, 0), (0, 1), (1, 1), (1, 2)], [(0, 0), (0, 1), (1, -1), (1, 0)], [(0, 0), (1, 0), (1, 1), (2, 1)], [(0, 0), (1, -1), (1, 0), (2, -1)]],#8
[[(0, 0), (0, 1), (1, -1), (1, 0), (2, 0)], [(0, 0), (1, -1), (1, 0), (2, 0), (2, 1)], [(0, 0), (1, 0), (1, 1), (2, -1), (2, 0)], [(0, 0), (0, 1), (1, 1), (1, 2), (2, 1)], [(0, 0), (1, -2), (1, -1), (1, 0), (2, -1)], [(0, 0), (1, -1), (1, 0), (1, 1), (2, 1)], [(0, 0), (1, -1), (1, 0), (1, 1), (2, -1)], [(0, 0), (1, 0), (1, 1), (1, 2), (2, 1)]],#9
[[(0, 0), (1, -1), (1, 0), (1, 1), (2, 0)]],#10
[[(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)], [(0, 0), (0, 1), (1, -1), (1, 0), (1, 1)], [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)], [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)], [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)], [(0, 0), (1, -1), (1, 0), (2, -1), (2, 0)], [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1)], [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]],#11
[[(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)], [(0, 0), (0, 1), (1, -1), (1, 0), (2, -1)], [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)], [(0, 0), (1, -1), (1, 0), (2, -2), (2, -1)]],#12
[[(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)], [(0, 0), (1, -2), (1, -1), (1, 0), (2, -2)], [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)], [(0, 0), (0, 1), (1, 0), (2, -1), (2, 0)]],#13
[[(0, 0), (0, 1), (0, 2), (0, 3), (1, 2)], [(0, 0), (1, -2), (1, -1), (1, 0), (1, 1)], [(0, 0), (1, -1), (1, 0), (1, 1), (1, 2)], [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1)], [(0, 0), (1, -1), (1, 0), (2, 0), (3, 0)], [(0, 0), (1, 0), (2, -1), (2, 0), (3, 0)], [(0, 0), (1, 0), (2, 0), (2, 1), (3, 0)], [(0, 0), (1, 0), (1, 1), (2, 0), (3, 0)]],#14
[[(0, 0), (1, 0), (1, 1), (1, 2), (1, 3)], [(0, 0), (0, 1), (0, 2), (0, 3), (1,0)], [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3)], [(0, 0), (1, -3), (1, -2), (1, -1), (1, 0)], [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)], [(0, 0), (0, 1), (1, 0), (2, 0), (3, 0)], [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1)], [(0, 0), (1, 0), (2, 0), (3, -1), (3, 0)]],#15
[[(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)], [(0, 0), (0, 1), (0, 2), (1, 0), (1,2)], [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)], [(0, 0), (0, 1), (1, 1), (2, 0),(2, 1)]],#16
[[(0, 0), (1, 0), (1, 1), (1, 2), (2, 0)], [(0, 0), (1, -2), (1, -1), (1, 0), (2, 0)], [(0, 0), (1, 0), (2, -1), (2, 0), (2, 1)], [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]],#17
[[(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)], [(0, 0), (1, 0), (2, 0), (2, 1), (2,2)], [(0, 0), (1, 0), (2, -2), (2, -1), (2, 0)], [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]],#18
[[(0, 0), (0, 1), (0, 2), (1, 2), (1, 3)], [(0, 0), (0, 1), (1, -2), (1, -1), (1, 0)], [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3)], [(0, 0), (0, 1), (0, 2), (1, -1), (1, 0)], [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1)], [(0, 0), (1, 0), (2, -1),(2, 0), (3, -1)], [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1)], [(0, 0), (1, -1), (1, 0), (2, -1), (3, -1)]],#19
[[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)], [(0, 0), (1, 0), (2, 0), (3, 0), (4,0)]])#20

# --------------------------------------------------

# --------------- class definitions ----------------

class GridBoard:
    """
    棋盘
    """
    EMPTY = -1
    NOTGOOD = -2
    def __init__(self, size):
        self.data = [[-1 for i in range(size)] for j in range(size)] # -1代表该grid为空
        self.size = size

    def __getitem__(self, index):
        return self.data.__getitem__(index)

    def __setitem__(self, key, item):
        self.data[key] = item

    def __str__(self):
        def numToStr(number):
            if number < 0:
                return "e"
            return str(number)
        out = [[numToStr(self.data[x][y])[0] for y in range(self.size)] for x in range(self.size)]
        return '\n'.join([''.join(x) for x in out])

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        if other == None: return False
        return self.data == other.data

    def copy(self):
        g = GridBoard(self.size)
        g.data = [x[:] for x in self.data]
        return g

    def getReverseBoard(self):
        g = GridBoard(self.size)
        tmp_dict = {1:0, 0:1, -1:-1}
        g.data = [[tmp_dict[i] for i in x] for x in self.data]
        for x in g.data:
            x.reverse()
        g.data.reverse()
        return g

    def deepCopy(self):
        return self.copy()

    def shallowCopy(self):
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def asList(self, num):
        listr = []
        for x in range(self.size):
            for y in range(self.size):
                if self[x][y] == num: listr.append( (x,y) )
        return listr

class GameStateData:
    def __init__(self, size = SIZE):
        self.leftPileList = [range(PILE_NUMBER), range(PILE_NUMBER)]
        self.boardData = GridBoard(size)

    def generateNextStateData(self, index, action):
        pileIndex, squarePos, rotateIndex = action
        localPosList = PileRotateList[pileIndex][rotateIndex]
        self.leftPileList[index].remove(pileIndex)
        for pos in localPosList:
            self.boardData[squarePos[0] + pos[0]][squarePos[1] + pos[1]] = index


    def deepCopy(self):
        g = GameStateData()
        g.leftPileList = [self.leftPileList[0][:], self.leftPileList[1][:]]
        g.boardData = self.boardData.deepCopy()
        return g


class GameState:
    """
    A GameState object contains all the information an agent need to know about the current game state,
    including
    1. Piles on the boards
    2. The left piles of each player
    """
    def __init__(self, oldState = None):
        self.legalActionsDict = dict()
        self.availDict = dict()
        self.impoDict = dict()

        if oldState is None:
            self.data = GameStateData()
        else:
            self.data = oldState.data.deepCopy()

    def getLegalActions(self, index):
        if self.legalActionsDict.has_key(index):
            return self.legalActionsDict[index]

        leftPiles = self.getLeftPiles(index)
        availGridList, impoGridSet = self._getAvailableAndImportantGrids(index)
        legalActions = []

        if not impoGridSet:
            return legalActions
        for pileIndex in leftPiles:
            for pos in availGridList:
                if min(map(lambda p: manhattanDistance(p, pos), impoGridSet)) > PileMaxManhattanList[pileIndex]:
                    continue
                for rotateIndex in range(len(PileRotateList[pileIndex])):
                    positionList = map(lambda p: (pos[0] + p[0], pos[1] + p[1]), PileRotateList[pileIndex][rotateIndex])
                    if set(positionList).issubset(availGridList) and impoGridSet.intersection(set(positionList)):
                        legalActions.append((pileIndex, pos, rotateIndex))

        self.legalActionsDict[index] = legalActions
        return legalActions

    def getLeftPiles(self, index):
        return self.data.leftPileList[index][:]

    def getBoard(self):
        return self.data.boardData

    def getScores(self, index):
        score = 0
        for i in range(len(self.data.leftPileList[index])):
            score += PileSquareNumberList[self.data.leftPileList[index][i]]
        return score

    def getBoard(self):
        return self.data.boardData

    def generateSuccessor(self, index, action):
        """Check the legality of the specific action of player <index>, if it's legal generate the successor state"""
        if action not in self.getLegalActions(index):
            printIllegalMove()
            return self

        successor = GameState(self)
        successor.data.generateNextStateData(index, action)
        return successor

    def getReverseState(self):
        reState = GameState()
        reData = self.data.deepCopy()
        reData.leftPileList.reverse()
        reData.boardData = reData.boardData.getReverseBoard()
        reState.data = reData
        return reState

    def __hash__(self):
        return self.getBoard().__hash__()

    def __eq__(self, other):
        return self.getBoard() == other.getBoard()
    # --- helper function ---
    def _getAvailableAndImportantGrids(self, index):
        """Get all the grids that the player <index> can place a squre on. Get the list of import grids of player <index>, in which a legal placement must cover at least one"""
       #if self.availDict.has_key(index) and self.impoDict.has_key(index):
        #    return self.availDict[index], self.impoDict[index]
        leftPiles = self.getLeftPiles(index)
        board = self.data.boardData.deepCopy()
        playerList = board.asList(index)
        importantGridSet = set()

        for point in playerList:
            for vector in NeighborVectors:
                pos = (point[0] + vector[0], point[1] + vector[1])
                if pos[0] not in range(0, board.size) or pos[1] not in range(0, board.size):
                    continue
                if board[pos[0]][pos[1]] == board.EMPTY:
                    board[pos[0]][pos[1]] = board.NOTGOOD
        for point in playerList:
            for vector in CrossVectors:
                pos = (point[0] + vector[0], point[1] + vector[1])
                if pos[0] < 0 or pos[0] >= board.size or pos[1] < 0 or pos[1] >= board.size:
                    continue
                if board[pos[0]][pos[1]] == board.EMPTY:
                    importantGridSet.add(pos)

        if len(leftPiles) == PILE_NUMBER: # Begining of the game
            importantGridSet = set([(0,0)]) if index == 0 else set([(self.data.boardData.size - 1, self.data.boardData.size - 1)])

        self.availDict[index] = board.asList(board.EMPTY)
        self.impoDict[index] = importantGridSet
        return self.availDict[index], self.impoDict[index]

    # -----------End helper function------------


# ----------------------End Class Definition----------------------------
