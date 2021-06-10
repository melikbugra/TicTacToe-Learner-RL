
class QLearningEnv:
    def __init__(self, index):
        self.reward_state_term = (None, None, None)
        self.index = index

    def getStateNum(self, index):
        return index

    def env_start(self):
        reward = 0
        state = self.getStateNum(self.index)
        termination = False
        self.reward_state_term = (reward, state, termination)

        return self.reward_state_term

    def env_step(self):

        reward = -10
        terminal = False

        self.reward_state_term = (reward, self.getStateNum(self.index), terminal)

        return self.reward_state_term

    def env_end(self, agentWins):
        if agentWins:
            terminal = True
            reward = 1000
        else:
            terminal = True
            reward = -10000

        self.reward_state_term = (reward, self.getStateNum(self.index), terminal)

        return self.reward_state_term
