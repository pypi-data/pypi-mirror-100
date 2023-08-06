import numpy
from Agents import IAgent
import random
from Rewards import RewardOnlyWinning

class AgentNaive_Random(IAgent.IAgent):

    def __init__(self, name="NAIVE_RANDOM"):

        self.name = "RANDOM_"+name
        self.reward = RewardOnlyWinning.RewardOnlyWinning()

    def getAction(self,  observations):

        possibleActions = observations[28:]

        itemindex = numpy.array(numpy.where(numpy.array(possibleActions) == 1))[0].tolist()

        random.shuffle(itemindex)
        aIndex = itemindex[0]
        a = numpy.zeros(200)
        a[aIndex] = 1

        return a

    def train(self, observations, nextobs, action, reward, info):
        pass

    def getReward(self, info):

        thisPlayer = info["thisPlayerPosition"]
        matchFinished = info["thisPlayerFinished"]

        return self.reward.getReward(thisPlayer, matchFinished)

