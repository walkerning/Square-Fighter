#!/usr/bin/env python
# -*- coding: utf-8 -*-

import AIagents
import game
import gameRunner
from learn import Learning

def default(string):
    return string + ' [Default: %default] '
def printResult(result, i = ''):
    if result[1] == -1:
        resultStr = "Tie!"
    else:
        resultStr = "agent%d Win!"%(result[1] + 1)
    print "No.%s: agent1 First: %s\n\tLeftSquares: %d -- %d"%(i, resultStr, result[-1][0], result[-1][1])

# 解析命令行参数
def ParseCommand(argv):
    from optparse import OptionParser

    # 命令行参数
    parser = OptionParser('')

    parser.add_option('-n', '--numGames', dest='numGames', type='int',
                      help=default('the number of GAMES to play'), metavar='GAMES', default=1)
    parser.add_option('--a1', '--agent1', dest='agent1', type='str',
                      help=default("agent1's name"), metavar='AGENTNAME',default='defaultAgent')
    parser.add_option('--a2', '--agent2', dest='agent2', type='str',
                      help=default("agent2's name"), metavar='AGENTNAME',default='defaultAgent')
    parser.add_option('-s', '--switch', action='store_true', dest='switch', help='play 2*n times with switching order')
    parser.add_option('-r', '--record', action='store_true', dest='record',
  help='Store replay files.', default=False)
    parser.add_option('-l', '--learn', action='store_true', dest='learn',
                      help='Learning algorithm')

    options, junk = parser.parse_args(argv)
    if len(junk) != 0:
        raise Exception('Command line input not understood: ' + str(junk))
    args = dict()
    args['record'] = options.record
    args['numGames'] = options.numGames
    args['agents'] = (options.agent1, options.agent2)
    args['switch'] = options.switch
    args['learn'] = options.learn

    return args

def runGames(agents, numGames, record, switch, learn):
    games = []

    if learn:
        Learning(numGames)
        return
    agentList = []
    for i in range(len(agents)):
        agent = agents[i]
        if not hasattr(AIagents, agent) or not hasattr(getattr(AIagents, agent), 'getAction'):
            printAgentError(agent)
            agent = "defaultAgent"
        agentList.append(getattr(AIagents, agent)(i))

    for i in range(numGames):
        game = gameRunner.Game(agentList, True)
        game.startGame()
        result = game.recordList[-1]
        printResult(result, str(i))
        if record:
            import time, cPickle
            filename = "%dtimes-"%numGames + "%s-vs-%s"%tuple([x.__class__.__name__ for x in agentList]) + time.strftime('%m-%d-%H-%M-%S',time.localtime(time.time())) + ".rep"
            f = file(filename, 'w')
            cPickle.dump(game.recordList, f)
            f.close()

    if switch:
        agentList = [agentList[1].__class__(0), agentList[0].__class__(1)]
        for i in range(numGames):
            game = gameRunner.Game(agentList, True)
            game.startGame()
            result = game.recordList[-1]
            if result[1] == -1:
                resultStr = "Tie!"
            else:
                resultStr = "agent%d Win!"%(2 - result[1])
                print "No.%d: agent2 First: %s\n\tLeftSquares: %d -- %d"%(i, resultStr, result[-1][1], result[-1][0])

            if record:
                import time, cPickle
                filename = "%dtimes-"%numGames + "%s-vs-%s"%tuple([x.__class__.__name__ for x in agentList]) + time.strftime('%m-%d-%H-%M-%S',time.localtime(time.time())) + ".rep"
                f = file(filename, 'w')
                cPickle.dump(game.recordList, f)
                f.close()

if __name__ == "__main__":
    # run game!
    import sys
    args = ParseCommand(sys.argv[1:])
    runGames(**args)
