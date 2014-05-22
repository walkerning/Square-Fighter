# -*- coding: utf-8 -*-

import gameRunner
import AIagents
import copy
import game

WIN_UTILITY = 1
TIE_UTILITY = 0
LOSE_UTILITY = -1
STEP1 = 0.01
STEP2 = 0.001
gameStateLib = [{} for x in range(21)]

def storeState(gameState, index):
	leftnum = len(gameState.getLeftPiles(index))
	if leftnum <= 17:
		value = evalFunc(gameState, index)
		if gameState not in gameStateLib[leftnum]:
			gameStateLib[leftnum][str(gameState)] = value
			print "gameStateLib is enlarged:",gameState," || ",value

def extractFeatures(gameState, index):
    avail_self, impo_self = gameState._getAvailableAndImportantGrids(index)
    avail_self, impo_self = float(len(avail_self))/10, len(impo_self)
    avail_oppo, impo_oppo = gameState._getAvailableAndImportantGrids(1 - index)
    avail_oppo, impo_oppo = float(len(avail_oppo))/10, len(impo_oppo)
    diff_square = gameState.getScores(1 - index) - gameState.getScores(index)
    #print "extract feats", (impo_self, impo_oppo, avail_self, avail_oppo, diff_square)
    return (impo_self, impo_oppo, avail_self, avail_oppo, diff_square)

def evalFunc(gameState, index):
    weights = [0.7317122, -1.951789, 0.1245964, -0.763426, 2.031588]
    featureList = extractFeatures(gameState, index)
    return sum(map(lambda x, y: x * y, featureList, weights))

def training(trainingDatas):
	for datum in trainingDatas:
		gameStateLib[datum[0].getLeftPiles(0)][str(datum(0))] += STEP2 * datum[2]

def Learning(times, learningAgent="ReflexStateAgent", start = []):
        if not hasattr(AIagents, learningAgent) or not hasattr(getattr(AIagents, learningAgent), 'getAction'):
            printAgentError(learningAgent)
            learningAgent = "ReflexStateAgent"
        agentClass = getattr(AIagents, learningAgent)

        agents = [agentClass(i, evalFunc) for i in range(2)]

        for i in range(times):
            trainingDatas = []

            game = gameRunner.Game(agents, True)
            game.startGame()
            recordList = copy.deepcopy(game.recordList)

            #printResult(recordList[-1], str(i))
            squareLost = game.leftSquares[0] - game.leftSquares[1]
            if recordList[-1][1] == -1:
                utilityList = [TIE_UTILITY, TIE_UTILITY]
            elif recordList[-1][1] == 0:
                squareLost = game.leftSquares[1] - game.leftSquares[0]
                #utilityList = [WIN_UTILITY + squareLost % 50, LOSE_UTILITY - squareLost % 50]
                utilityList = [WIN_UTILITY, LOSE_UTILITY]
            else:
                #utilityList = [LOSE_UTILITY - squareLost % 50, WIN_UTILITY + squareLost % 50]
                utilityList = [LOSE_UTILITY, WIN_UTILITY]
            recordList.pop()
            for i in range(len(recordList)):
                record = recordList[i]
                storeState(record[4], record[0])
            	trainingDatas.append((record[-1], record[0], squareLost))
            Training(trainingDatas, weights)




