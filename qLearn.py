# -*- coding: utf-8 -*-

import gameRunner
import AIagents
import copy
from loopLearn import printResult

R = 0.9
SQUARE_TOTAL = 89
INI_WEIGHT = (1.0516153729117497, -1.7406298037151497, 2.2668134620369664, -1.705074288351434)
WIN_UTILITY = 100
LOSE_UTILITY = -100
TIE_UTILITY = 0

DATA_FILENAME = "q.data"

class StateLib(dict):
    def __init__(self, evalFunc):
        super(StateLib, self).__init__()

        self.evalFunc = evalFunc

    def __getitem__(self, key):
        if key not in self:
            #print "default evalfunc"
            #return [self.evalFunc(key, i, INI_WEIGHT) for i in range(2)]
            return [self.evalFunc(key, i) for i in range(2)]
        else:
            #print "key in!"
            return super(StateLib, self).__getitem__(key)

def extractFeatures(gameState, index):
    avail_self, impo_self = gameState._getAvailableAndImportantGrids(index)
    avail_self, impo_self = float(len(avail_self))/10, len(impo_self)
    avail_oppo, impo_oppo = gameState._getAvailableAndImportantGrids(1 - index)
    avail_oppo, impo_oppo = float(len(avail_oppo))/10, len(impo_oppo)
    square_self = SQUARE_TOTAL - gameState.getScores(index)
    square_oppo = SQUARE_TOTAL - gameState.getScores(1 - index)
    #diff_square = gameState.getScores(1 - index) - gameState.getScores(index)
    #print "extract feats", (impo_self, impo_oppo, avail_self, avail_oppo, diff_square)
    return (impo_self, impo_oppo, square_self, square_oppo)#diff_square)#avail_self, avail_oppo, diff_square)

def immediatePayback(gameState, index):#, index, action):
    return evalFunc(gameState, index, INI_WEIGHT) - evalFunc(gameState, 1 - index, INI_WEIGHT)
    nextState = gameState.generateSuccessor(index, action)
    (_, impo_oppo_next) = nextState._getAvailableAndImportantGrids(1 - index)
    (_, impo_oppo) = gameState._getAvailableAndImportantGrids(index)
    return impo_oppo - impo_oppo_next

def evalFunc(gameState, index, weights):
    #return 0
    featureList = extractFeatures(gameState, index)
    return sum(map(lambda x, y: x * y, featureList, weights))


def Training(trainingDatas, RawStateLib, finalUtility):
    RawStateLib[trainingDatas[0][0]] = finalUtility[:]
    RawStateLib[trainingDatas[0][0].getReverseState()] = [finalUtility[1], finalUtility[0]]
    for i in range(1, len(trainingDatas)):
        datum = trainingDatas[i][0]
        playerIndex = trainingDatas[i][1]
        uPrimeList = []
        for action in datum.getLegalActions(playerIndex):
            newState = datum.generateSuccessor(playerIndex, action)
            tmp = RawStateLib[newState][playerIndex]
            uPrimeList.append(tmp)
        #感觉需要两边对称更新才有用
        if not uPrimeList:
            uPrimeList = [0]
        if datum not in  RawStateLib:
            #if max(uPrimeList):
                #print max(uPrimeList)
            #RawStateLib[datum][playerIndex] = immediatePayback(datum, playerIndex) + R * max(uPrimeList)
            #print "imm:", immediatePayback(datum, playerIndex)
            RawStateLib[datum] = [immediatePayback(datum, playerIndex) + R * max(uPrimeList),-immediatePayback(datum, playerIndex)-R * max(uPrimeList)]
            reDatum = datum.getReverseState()
            RawStateLib[reDatum] = [-R * max(uPrimeList) - immediatePayback(datum, playerIndex), immediatePayback(datum, playerIndex) + R * max(uPrimeList)]
        else:
            #要不要考虑一下用和为0的权值
            #if max(uPrimeList):
                #print max(uPrimeList)
            #print "imm:", immediatePayback(datum, playerIndex)
            RawStateLib[datum][0] = immediatePayback(datum, playerIndex) + R * max(uPrimeList)#evalFunc(datum, 1, INI_WEIGHT)]
            RawStateLib[datum][1] = - RawStateLib[datum][0]
            reDatum = datum.getReverseState()
            RawStateLib[reDatum][1] = immediatePayback(datum, playerIndex) + R * max(uPrimeList)
            RawStateLib[reDatum][0] = - RawStateLib[reDatum][1]


def Learning(times, learningAgent="qLearnAgent", start = StateLib(immediatePayback)):
    if not hasattr(AIagents, learningAgent) or not hasattr(getattr(AIagents, learningAgent), 'getAction'):
        printAgentError(learningAgent)
        learningAgent = "qLearnAgent"
    agentClass = getattr(AIagents, learningAgent)

    lib = start
    agents = [agentClass(i, True) for i in range(2)]

    for i in range(times):
        trainingDatas = []
        for agent in agents:
            agent.setLib(lib)
        game = gameRunner.Game(agents, True)
        game.startGame()
        recordList = copy.deepcopy(game.recordList)

        printResult(recordList[-1], str(i))
        #import time, cPickle
        #filename = "qlearn--No.%d--"%i + time.strftime('%m-%d-%H-%M-%S',time.localtime(time.time())) + ".rep"
        #f = file(filename, 'w')
        #cPickle.dump(game.recordList, f)
        #f.close()
        if recordList[-1][1] == -1:
            utilityList = [TIE_UTILITY, TIE_UTILITY]
        elif recordList[-1][1] == 0:
            squareLost = game.leftSquares[1] - game.leftSquares[0]
            #utilityList = [WIN_UTILITY + squareLost % 50, LOSE_UTILITY - squareLost % 50]
            utilityList = [WIN_UTILITY, LOSE_UTILITY]
        else:
            squareLost = game.leftSquares[0] - game.leftSquares[1]
            utilityList = [LOSE_UTILITY, WIN_UTILITY]
        recordList.pop()
        for i in range(0, len(recordList) - 1):
            record = recordList[i]
            trainingDatas.insert(0, (record[-1], recordList[i + 1][0]))
        trainingDatas.insert(0, (recordList[-1][-1], None))
        oldLib = copy.deepcopy(lib)
        Training(trainingDatas, lib, utilityList)
        #print "oldLib", oldLib
        #print "newLib", lib
        #print "oldLib = lib?", oldLib == lib
        #print "oldLIb.keys() = lib.keys()?", oldLib.keys() == lib.keys()
    import cPickle
    f = file(DATA_FILENAME, 'w')
    cPickle.dump(lib, f)
    f.close()
