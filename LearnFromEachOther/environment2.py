
class QLearningEnv2:
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

        reward = -1
        terminal = False

        self.reward_state_term = (reward, self.getStateNum(self.index), terminal)

        return self.reward_state_term

    def env_end(self, agentWins):
        if agentWins == 1:
            terminal = True
            reward = 200
        elif agentWins == 2:
            terminal = True
            reward = -200
        else:
            terminal = True
            reward = -300

        self.reward_state_term = (reward, self.getStateNum(self.index), terminal)

        return self.reward_state_term
