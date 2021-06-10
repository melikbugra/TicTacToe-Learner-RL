import numpy as np
import pickle


class QLearningAgent:
    def __init__(self, info):
        self.num_actions = info[0]
        self.epsilon = info[1]
        self.step_size = info[2]
        self.discount = info[3]
        self.rand_generator = np.random.RandomState(info[4])
        self.prev_state = 0
        self.prev_action = 0

        with open("qMatrix.txt", "rb") as fp:
            self.q = pickle.load(fp)

    def agent_start(self, state):
        # Choose action using epsilon greedy.
        current_q = self.q[state, :]
        if self.rand_generator.rand() < self.epsilon:
            action = self.rand_generator.randint(self.num_actions)
        else:
            action = self.argmax(current_q)
        self.prev_state = state
        self.prev_action = action
        return action

    def agent_start_first(self, state):
        # Choose action using epsilon greedy.
        current_q = self.q[state, :]
        if self.rand_generator.rand() < self.epsilon:
            action = self.rand_generator.randint(self.num_actions)
        else:
            action = self.argmax(current_q)
        self.prev_state = state + 1
        self.prev_action = action + 1
        return action

    def agent_step(self, reward, state):
        # Choose action using epsilon greedy.
        current_q = self.q[state, :]
        if self.rand_generator.rand() < self.epsilon:
            action = self.rand_generator.randint(self.num_actions)
            print('*******RANDOM ACTION**********')
        else:
            action = self.argmax(current_q)

        self.q[self.prev_state, self.prev_action] = self.q[self.prev_state, self.prev_action] + self.step_size * (
                    reward + self.discount * max(current_q) - self.q[self.prev_state, self.prev_action])

        self.prev_state = state
        self.prev_action = action

        return action

    def argmax(self, q_values):
        top = float("-inf")
        ties = []

        for i in range(len(q_values)):
            if q_values[i] > top:
                top = q_values[i]
                ties = []

            if q_values[i] == top:
                ties.append(i)

        return self.rand_generator.choice(ties)

    def agent_end(self, reward):

        self.q[self.prev_state, self.prev_action] = self.q[self.prev_state, self.prev_action] + self.step_size * (
                    reward - self.q[self.prev_state, self.prev_action])

        # print(self.step_size * (
        #             reward - self.q[self.prev_state, self.prev_action]))
        # print('\n', '   ', self.prev_state, '   ', self.prev_action, self.q[self.prev_state, self.prev_action])

        with open("qMatrix.txt", "wb") as fp:
            pickle.dump(self.q, fp)
