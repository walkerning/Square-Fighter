# -*- coding: utf-8 -*-

import gameRunner
import AIagents
import copy

SQUARE_TOTAL = 89
WIN_UTILITY = 30#50
TIE_UTILITY = 0
LOSE_UTILITY = -30#-50
R = 0.9
STEP = 0.0001
FEATURES = ('impo_self','impo_oppo','square_self','square_oppo')#, 'diff_square')
STARTING_WEIGHT = (0.9, -0.9, 1, -1)#0.5, -0.5, 1)

def printResult(result, i = ''):
    if result[1] == -1:
        resultStr = "Tie!"
    else:
        resultStr = "agent%d Win!"%(result[1])
    print "No.%s: agent0 First: %s\n\tLeftSquares: %d -- %d"%(i, resultStr, result[-1][0], result[-1][1])

def extractFeatures(gameState, index):
    avail_self, impo_self = gameState._getAvailableAndImportantGrids(index)
    avail_self, impo_self = float(len(avail_self))/10, len(impo_self)
    avail_oppo, impo_oppo = gameState._getAvailableAndImportantGrids(1 - index)
    avail_oppo, impo_oppo = float(len(avail_oppo))/10, len(impo_oppo)
    square_self = SQUARE_TOTAL - gameState.getScores(index)
    square_oppo = SQUARE_TOTAL - gameState.getScores(1 - index)
    diff_square = gameState.getScores(1 - index) - gameState.getScores(index)
    #return (impo_self, impo_oppo, avail_self, avail_oppo, diff_square)#print "extract feats", 
    return (impo_self, impo_oppo, square_self, square_oppo)#,diff_square)#avail_self, avail_oppo, diff_square)

def evalFunc(gameState, index, weights):
    featureList = extractFeatures(gameState, index)
    return sum(map(lambda x, y: x * y, featureList, weights))

def immediatePayback(gameState, index, action):
    nextState = gameState.generateSuccessor(index, action)
    (_, impo_oppo_next) = nextState._getAvailableAndImportantGrids(1 - index)
    (_, impo_oppo) = gameState._getAvailableAndImportantGrids(index)
    return impo_oppo - impo_oppo_next

def Training(trainingDatas, weights):
    for datum in trainingDatas:
        feats = extractFeatures(datum[0], datum[1])
        nowUti = sum(map(lambda x, y: x * y, feats, weights))
        newUti = datum[2]

        #print "cha:",newUti - nowUti
        for i in range(len(weights)):
            if i == 0 and feats[2] >= 50:
                continue
            weights[i] += STEP * feats[i] * (R * newUti - nowUti)

def Learning(times, learningAgent="ReflexLinearAgent", start = [0.902986552409241, -3.44081507944618, 1.9210094578349792, -1.4626332827670643]):#[1.3290, -2.91247, 1.612913, -1.09355]):
        if not hasattr(AIagents, learningAgent) or not hasattr(getattr(AIagents, learningAgent), 'getAction'):
            printAgentError(learningAgent)
            learningAgent = "ReflexLinearAgent"
        agentClass = getattr(AIagents, learningAgent)

        weights = list(STARTING_WEIGHT if not start else start)
        print "starting weights:", weights
        agents = [agentClass(i, evalFunc) for i in range(2)]

        for i in range(times):
            trainingDatas = []
            for agent in agents:
                agent.setWeight(weights)
            game = gameRunner.Game(agents, True)
            game.startGame()
            recordList = copy.deepcopy(game.recordList)

            printResult(recordList[-1], str(i))
            if recordList[-1][1] == -1:
                utilityList = [TIE_UTILITY, TIE_UTILITY]
            elif recordList[-1][1] == 0:
                squareLost = game.leftSquares[1] - game.leftSquares[0]
                utilityList = [WIN_UTILITY - game.leftSquares[0] / 3.0, LOSE_UTILITY - game.leftSquares[1] / 3.0]
                #utilityList = [WIN_UTILITY, LOSE_UTILITY]
            else:
                squareLost = game.leftSquares[0] - game.leftSquares[1]
                utilityList = [LOSE_UTILITY - game.leftSquares[0]/3.0, WIN_UTILITY -game.leftSquares[1]/3.0]
                #utilityList = [LOSE_UTILITY, WIN_UTILITY]
            recordList.pop()
            for i in range(len(recordList)/3, len(recordList)):
                record = recordList[i]
                j = i
                while True:
                    if j == len(recordList) - 1 or recordList[j + 1][0] == record[0]:
                        break
                    j += 1
                if j == len(recordList) - 1:
                    newUti = utilityList[record[0]]
                else:
                    newUti = evalFunc(recordList[j][-1], record[0], weights)
                trainingDatas.append((record[-1], record[0], newUti))
            Training(trainingDatas, weights)
            print "weights updated", weights


        print "result weights:", weights
