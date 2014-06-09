# -*- coding: utf-8 -*-

import gameRunner
import AIagents
import copy
from loopLearn import printResult

MAGIC_STRING = "LEARN PATTERN FILE\n"
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
            return self.evalFunc(key, 0)
        else:
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
    featureList = extractFeatures(gameState, index)
    return sum(map(lambda x, y: x * y, featureList, weights))


def Training(trainingDatas, RawStateLib, finalUtility):
    RawStateLib[trainingDatas[0][0]] = finalUtility[0]
    RawStateLib[trainingDatas[0][0].getReverseState()] = [finalUtility[1], finalUtility[0]]
    for i in range(1, len(trainingDatas)):
        datum = trainingDatas[i][0]
        playerIndex = trainingDatas[i][1]
        uPrimeList = []
        for action in datum.getLegalActions(playerIndex):
            newState = datum.generateSuccessor(playerIndex, action)
            tmp = (1 - 2 * playerIndex) * RawStateLib[newState]
            uPrimeList.append(tmp)
        #感觉需要两边对称更新才有用
        '''
        <<<<<<< HEAD
                #if not uPrimeList:
                    #uPrimeList = [0]
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

                        #RawStateLib[datum][playerIndex] = immediatePayback(datum, playerIndex) + R * max(uPrimeList)
                        #print "imm:", immediatePayback(datum, playerIndex)
                        RawStateLib[datum] = [immediatePayback(datum, playerIndex) + R * max(uPrimeList), -immediatePayback(datum, playerIndex)-R * max(uPrimeList)]
                        #print "max uprime:", max(uPrimeList), "imm:", immediatePayback(datum, playerIndex) ,"new datum:",RawStateLib[datum]
                        reDatum = datum.getReverseState()
                        RawStateLib[reDatum] = [-R * max(uPrimeList) - immediatePayback(datum, playerIndex), immediatePayback(datum, playerIndex) + R * max(uPrimeList)]
                    
                else:
                    #if max(uPrimeList):
                    #print max(uPrimeList)

                    #print "imm:", immediatePayback(datum, playerIndex)
                    RawStateLib[datum][0] = immediatePayback(datum, playerIndex) + R * max(uPrimeList)#evalFunc(datum, 1, INI_WEIGHT)]
                    RawStateLib[datum][1] = - RawStateLib[datum][0]
                    reDatum = datum.getReverseState()
                    RawStateLib[reDatum][1] = immediatePayback(datum, playerIndex) + R * max(uPrimeList)
                    RawStateLib[reDatum][0] = - RawStateLib[reDatum][1]
        =======
        '''
        RawStateLib[datum] = (1 - 2 * playerIndex) * (immediatePayback(datum, playerIndex) + R * max(uPrimeList))
        RawStateLib[datum.getReverseState()] = -RawStateLib[datum]
        


def Learning(times, learningAgent="qLearnAgent", learn_pattern = None, start_file = ''):
    if not hasattr(AIagents, learningAgent) or not hasattr(getattr(AIagents, learningAgent), 'getAction'):
        printAgentError(learningAgent)
        learningAgent = "qLearnAgent"
    agentClass = getattr(AIagents, learningAgent)

    # 导入已有数据
    if not start_file:
        lib = StateLib(immediatePayback)
    else:
        import cPickle
        f = open(start_file)
        try:
            lib = cPickle.load(f)
        except:
            print "load base file fail, fall back to empty base lib"
            pass
        finally:
            f.close()

    learnPattern = []
    # 分析训练模式文件
    if learn_pattern:
        f = open(learn_pattern)
        magic_line = f.readline()
        if magic_line != MAGIC_STRING:
            print "文件格式错误:训练模式文件必须以'LEARN PATTERN FILE'作为第一行"
            exit(0)
        import re
        x1 = re.compile(r'\s+')
        x2 = re.compile(r'\n')
        for line in f.readlines():
            line,_ = x2.subn('', line)
            line = x1.split(line)
            if '' in line:
                line.remove('')
            learnPattern.append(map(lambda x: eval(x), line))
        curPattern = learnPattern.pop(0)
        agents = [None, None]
        if len(curPattern) == 3:
            agents[curPattern[1]] = getattr(AIagents, learningAgent)(curPattern[1], True)
            agents[1 - curPattern[1]] = getattr(AIagents, curPattern[2])(1 - curPattern[1])
        elif len(curPattern) == 1:
            agents = [agentClass(i, True) for i in range(2)]
        else:
            pass#wrong
        print curPattern
        f.close()
    else:
        agents = [agentClass(i, True) for i in range(2)]


    for i in range(times):
        trainingDatas = []
        if learn_pattern:
            curPattern[0] -= 1
            if curPattern[0] < 0:
                if learnPattern:
                    curPattern = learnPattern.pop(0)
                    print curPattern
                    if len(curPattern) == 3:
                        agents[curPattern[1]] = getattr(AIagents, learningAgent)(curPattern[1], True)
                        agents[curPattern[1]].setLib(lib)
                        agents[1 - curPattern[1]] = getattr(AIagents, curPattern[2])(1 - curPattern[1])
                    elif len(curPattern) == 1:
                        agents = [agentClass(j, True) for j in range(2)]
                        for agent in agents:
                            agent.setLib(lib)
                    else:
                        pass#wrong
                    curPattern[0] -= 1
                else:
                    learn_pattern = None
                    agents = [agentClass(j ,True) for j in range(2)]
                    for agent in agents:
                        agent.setLib(lib)
            else:
                if len(curPattern) == 3:
                    agents[curPattern[1]].setLib(lib)
                elif len(curPattern) == 1:
                    for agent in agents:
                        agent.setLib(lib)
                else:
                    pass#wrong
        else:
            for agent in agents:
                agent.setLib(lib)
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
            utilityList = [LOSE_UTILITY, WIN_UTILITY]
        recordList.pop()
        for i in range(0, len(recordList) - 1):
            record = recordList[i]
            trainingDatas.insert(0, (record[-1], recordList[i + 1][0]))
        trainingDatas.insert(0, (recordList[-1][-1], None))
        oldLib = copy.deepcopy(lib)
        Training(trainingDatas, lib, utilityList)

    import cPickle
    f = file(DATA_FILENAME, 'w')
    cPickle.dump(lib, f)
    f.close()
