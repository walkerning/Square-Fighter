# -*- coding: utf-8 -*-

import gameRunner
import AIagents
import copy



def Learning(times, learningAgent="ReflexLinearAgent", start=[]):
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

            #printResult(recordList[-1], str(i))
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
