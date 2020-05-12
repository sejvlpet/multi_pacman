import random

"""
    stats about game
"""
class Stats:
    def __init__(self, gameStats):
        self.initialPillsEaten = gameStats["pillsEaten"]
        self.initialRounds = gameStats["round"]
        self.initialPacmansEaten = gameStats["pacmansEaten"]
        self.initialLooses = gameStats["looses"]
        self.initialWins = gameStats["wins"]

        self.rounds = 0
        self.pillsEaten = 0
        self.pacmansEaten = 0
        self.looses = 0
        self.wins = 0
        self.firsts = 0

        self.visitedTimes = 0

    def saveVisit(self, gameStats):
        self.pillsEaten += gameStats["pillsEaten"] - self.initialPillsEaten
        self.rounds += gameStats["round"] - self.initialRounds
        self.pacmansEaten += gameStats["pacmansEaten"] - self.initialPillsEaten
        self.looses += gameStats["looses"] - self.initialLooses
        self.wins += gameStats["wins"] - self.initialWins
        self.firsts += gameStats["firstEatenAt"]
        self.visitedTimes += 1

    def getScore(self):
        return Score(self)

    def getRandomMetric(self):
        if self.visitedTimes == 0:
            return random.randint(1000, 10000)
        res = (self.__getMetric() ** 2) * random.random()
        return res

    def __getMetric(self):
        if self.visitedTimes == 0:
            return 0

        metric = (self.__mean(self.pillsEaten) / self.__mean(self.rounds)
            - self.__mean(self.pacmansEaten) * self.__mean(self.rounds)) * self.__mean(self.firsts)
        if self.wins > 0:
            return 100000 - self.__mean(self.rounds)
        if self.looses > 0:
            return self.__mean(self.rounds)

        return metric

    def __mean(self, val):
        return val / self.visitedTimes


"""
    holds score taken from stats and can compare itself
"""
class Score:
    """
        takes stats and saves what it needs
    """
    def __init__(self, stats):
        self.stats = stats

    """
        compares two scores
    """
    def __gt__(self, other):
        sStats = self.stats
        oStats = other.stats

        if sStats.visitedTimes == 0:
            return False
        if oStats.visitedTimes == 0:
            return True

        sMetric = (self.__mean(sStats.pillsEaten) / self.__mean(sStats.rounds) - self.__mean(sStats.pacmansEaten) \
                  * self.__mean(sStats.rounds)) * self.__mean(sStats.firsts)
        oMetric = (other.__mean(oStats.pillsEaten) / other.__mean(oStats.rounds) - other.__mean(oStats.pacmansEaten) \
                  * other.__mean(oStats.rounds)) * other.__mean(oStats.firsts)
        if self.__mean(sStats.wins) > 0 and other.__mean(oStats.wins) <= 0:
            return True
        if self.__mean(sStats.wins) <= 0 and other.__mean(oStats.wins) > 0:
            return False
        if self.__mean(sStats.wins) > 0 and other.__mean(oStats.wins) > 0:
            # if this game is about to be won, choose the quickest solution
            return self.__mean(sStats.rounds) < other.__mean(oStats.rounds)

        if self.__mean(sStats.pillsEaten) == other.__mean(oStats.pillsEaten) and \
                self.__mean(sStats.pacmansEaten) == other.__mean(oStats.pillsEaten):
            return self.__mean(sStats.firsts) < other.__mean(oStats.firsts)

        return sMetric > oMetric

    def __mean(self, val):
        return val / self.stats.visitedTimes
