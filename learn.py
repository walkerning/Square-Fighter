# -*- coding: utf-8 -*-

import gameRunner
import AIagents
import copy

WIN_UTILITY = 100
TIE_UTILITY = 0
LOSE_UTILITY = -100
STEP = 0.0001
FEATURES = ('impo_self','impo_oppo','avail_self','avail_oppo','diff_square')
STARTING_WEIGHT = (0.9, -0.9, 0.5, -0.5, 1)

def extractFeatures(gameState, index):
    avail_self, impo_self = gameState._getAvailableAndImportantGrids(index)
    avail_self, impo_self = float(len(avail_self))/10, len(impo_self)
    avail_oppo, impo_oppo = gameState._getAvailableAndImportantGrids(1 - index)
    avail_oppo, impo_oppo = float(len(avail_oppo))/10, len(impo_oppo)
    diff_square = gameState.getScores(1 - index) - gameState.getScores(index)
    #print "extract feats", (impo_self, impo_oppo, avail_self, avail_oppo, diff_square)
    return (impo_self, impo_oppo, avail_self, avail_oppo, diff_square)

def evalFunc(gameState, index, weights):
    featureList = extractFeatures(gameState, index)
    return sum(map(lambda x, y: x * y, featureList, weights))


def Training(trainingDatas, weights):
    for datum in trainingDatas:
        feats = extractFeatures(datum[0], datum[1])
        nowUti = sum(map(lambda x, y: x * y, feats, weights))
        newUti = datum[2]

        #print "cha:",newUti - nowUti
        for i in range(len(weights)):
            weights[i] += STEP * feats[i] * (newUti - nowUti)

def Learning(times, learningAgent="ReflexLinearAgent", start = []):
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
                #utilityList = [WIN_UTILITY + squareLost % 50, LOSE_UTILITY - squareLost % 50]
                utilityList = [WIN_UTILITY, LOSE_UTILITY]
            else:
                squareLost = game.leftSquares[0] - game.leftSquares[1]
                #utilityList = [LOSE_UTILITY - squareLost % 50, WIN_UTILITY + squareLost % 50]
                utilityList = [LOSE_UTILITY, WIN_UTILITY]
            recordList.pop()
            for i in range(len(recordList)/2, len(recordList)):
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