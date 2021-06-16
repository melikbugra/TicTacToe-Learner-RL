import pygame
import os
from grid import Grid
import numpy as np
import copy
from environment import QLearningEnv
from environment2 import QLearningEnv2
from qlearningagent import QLearningAgent
from qlearningagent2 import QLearningAgent2
import pickle
import matplotlib.pyplot as plt

os.environ['SDL_VIDEO_WINDOW_POS'] = '600,200'

surface = pygame.display.set_mode((600, 600))
pygame.display.set_caption('TicTacToe')

grid = Grid()
a = [[]]
running = True
player = 'X'
with open("states.txt", "rb") as fp:
    states = pickle.load(fp)
with open("states2.txt", "rb") as fp:
    states2 = pickle.load(fp)


grid.game_over = True
eps = 0
step = 0.1
disc = 0.9
agentInfo = [9, eps, step, disc, 0]
currentState = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
env = QLearningEnv(states.index([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
env2 = QLearningEnv2(states.index([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
qAgent = QLearningAgent(agentInfo)
qAgent2 = QLearningAgent2(agentInfo)
with open("qMatrix.txt", "rb") as fp:
    qAgent.q = pickle.load(fp)
with open("qMatrix2.txt", "rb") as fp:
    qAgent2.q = pickle.load(fp)


def agentPlay(rew, stt):
    act = qAgent.agent_step(rew, stt)

    x = int(act % 3)
    y = int((act - x) / 3)

    bools = grid.get_cell_value(x, y) == 'X' or grid.get_cell_value(x, y) == 'O'
    while(bools):
        qAgent.q[stt, act] -= 100
        act = qAgent.agent_step(rew, stt)

        x = int(act % 3)
        y = int((act - x) / 3)
        bools = grid.get_cell_value(x, y) == 'X' or grid.get_cell_value(x, y) == 'O'

    if grid.get_cell_value(x, y) == 0:
        grid.switchPlayer = True

    grid.set_cell_value(x, y, 'O')
    grid.check_grid(x, y, player)

    return act

def agentStart(stt):
    act = qAgent.agent_start(stt)

    x = int(act % 3)
    y = int((act - x) / 3)

    bools = grid.get_cell_value(x, y) == 'X' or grid.get_cell_value(x, y) == 'O'
    while (bools):
        qAgent.q[stt, act] -= 100
        act = qAgent.agent_start(stt)

        x = int(act % 3)
        y = int((act - x) / 3)
        bools = grid.get_cell_value(x, y) == 'X' or grid.get_cell_value(x, y) == 'O'

    grid.set_cell_value(x, y, 'O')

    return act

def agentPlay2(rew, stt):
    act = qAgent2.agent_step(rew, stt)

    x = int(act % 3)
    y = int((act - x) / 3)

    bools = grid.get_cell_value(x, y) == 'X' or grid.get_cell_value(x, y) == 'O'
    while(bools):
        qAgent2.q[stt, act] -= 100
        act = qAgent2.agent_step(rew, stt)

        x = int(act % 3)
        y = int((act - x) / 3)
        bools = grid.get_cell_value(x, y) == 'X' or grid.get_cell_value(x, y) == 'O'

    if grid.get_cell_value(x, y) == 0:
        grid.switchPlayer = True

    grid.set_cell_value(x, y, 'X')
    grid.check_grid(x, y, player)

    return act

def agentStart2(stt):
    act = qAgent2.agent_start(stt)
    qAgent2.q[stt, act] -= 100

    x = int(act % 3)
    y = int((act - x) / 3)

    bools = grid.get_cell_value(x, y) == 'X' or grid.get_cell_value(x, y) == 'O'
    while (bools):
        act = qAgent2.agent_start(stt)

        x = int(act % 3)
        y = int((act - x) / 3)
        bools = grid.get_cell_value(x, y) == 'X' or grid.get_cell_value(x, y) == 'O'

    grid.set_cell_value(x, y, 'X')

    return act


score = 0
with open("scores.txt", "rb") as fp:
    scores = pickle.load(fp)
with open("iteration.txt", "rb") as fp:
    iteration = pickle.load(fp)
pause = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                with open("qMatrix2.txt", "wb") as fp:
                    pickle.dump(qAgent2.q, fp)
                with open("qMatrix.txt", "wb") as fp:
                    pickle.dump(qAgent.q, fp)
                with open("scores.txt", "wb") as fp:
                    pickle.dump(scores, fp)
                if pause:
                    pause = False
                elif not pause:
                    pause = True
    if grid.game_over or iteration == 0:
        currentState2 = copy.deepcopy(grid.grid)
        if currentState2 not in states2:
            qAgent2.q = np.vstack((qAgent2.q, [0, 0, 0, 0, 0, 0, 0, 0, 0]))
            states2.append(currentState2)
        stt2 = env2.getStateNum(states2.index(currentState2))
        act2 = agentStart2(stt2)
        rew2 = env2.env_step()[0]
        player = 'O'
        currentState = copy.deepcopy(grid.grid)
        if currentState not in states:
            qAgent.q = np.vstack((qAgent.q, [0, 0, 0, 0, 0, 0, 0, 0, 0]))
            states.append(currentState)
        stt = env.getStateNum(states.index(currentState))
        act = agentStart(stt)
        rew = env.env_step()[0]
        grid.switchPlayer = True
        grid.game_over = False

    while not pause and not grid.game_over:
        with open("iteration.txt", "rb") as fp:
            iteration = pickle.load(fp)
        if grid.switch_player:
            if player == 'X':
                player = 'O'
            else:
                player = 'X'

        if player == 'O':
            currentState = copy.deepcopy(grid.grid)
            aaaaa = states


            if currentState not in states:
                qAgent.q = np.vstack((qAgent.q, [0, 0, 0, 0, 0, 0, 0, 0, 0]))
                with open("qMatrix.txt", "wb") as fp:
                    pickle.dump(qAgent.q, fp)
                states.append(currentState)
                with open("states.txt", "wb") as fp:
                    pickle.dump(states, fp)

        if not grid.game_over and player == 'O':
            env = QLearningEnv(states.index(currentState))
            stt = env.getStateNum(states.index(currentState))
            act = agentPlay(rew, stt)
            actt = act
            xxd = qAgent.prev_action
            rew = env.env_step()[0]
            score += rew
            # print('\n', currentState, '    no= ', states.index(currentState), '     i=  ', iteration)
            # print('\n', qAgent.q[stt], stt)
            # # print('\n', qAgent.q)
            # print('act= ', act)
            # print('stt= ', stt)
            with open("qMatrix.txt", "wb") as fp:
                pickle.dump(qAgent.q, fp)
            # print('rew', rew)
            # print('stt', len(states))
            # print('q', len(qAgent.q))

            if grid.switch_player:
                if player == 'X':
                    player = 'O'
                else:
                    player = 'X'
        if player == 'X':
            currentState2 = copy.deepcopy(grid.grid)
            aaaa = states2

            if currentState2 not in states2:
                qAgent2.q = np.vstack((qAgent2.q, [0, 0, 0, 0, 0, 0, 0, 0, 0]))
                with open("qMatrix2.txt", "wb") as fp:
                    pickle.dump(qAgent2.q, fp)
                states2.append(currentState2)
                with open("states2.txt", "wb") as fp:
                    pickle.dump(states2, fp)



        if not grid.game_over and player == 'X':
            env2 = QLearningEnv2(states2.index(currentState2))
            stt2 = env2.getStateNum(states2.index(currentState2))
            act2 = agentPlay2(rew2, stt2)
            actt2 = act2
            rew2 = env2.env_step()[0]
            # print('\n\n\nPlayer X')
            # print('\n', currentState2, '    no2= ', states2.index(currentState2), '     i=  ', iteration)
            # print('\n', qAgent2.q[stt2], stt2)
            # print('act2= ', act2)
            # print('stt2= ', stt2)
            with open("qMatrix2.txt", "wb") as fp:
                pickle.dump(qAgent2.q, fp)
            # print('rew2', rew2)
            # print('stt2', len(states2))
            # print('q2', len(qAgent2.q))

    if grid.game_over:
        # print('             ', iteration)
        print('                                  stt= ', stt)
        rew = env.env_end(grid.oWins)[0]
        qAgent.agent_end(rew)
        rew2 = env2.env_end(grid.xWins)[0]
        qAgent2.agent_end(rew2)
        score += rew
        grid.clear_grid()
        # stt2 = env2.env_start()[1]
        # rew2 = env2.env_start()[0]
        # act2 = qAgent2.agent_start(stt2)
        # xStart = int(act2 % 3)
        # yStart = int((act2 - xStart) / 3)
        grid.switchPlayer = True
        # grid.set_cell_value(xStart, yStart, 'X')
        player = 'O'
        iteration += 1
        with open("iteration.txt", "wb") as fp:
            pickle.dump(iteration, fp)
        scores.append(score)
        with open("scores.txt", "wb") as fp:
            pickle.dump(scores, fp)
        score = 0


    surface.fill((0, 0, 0))

    grid.draw(surface)

    pygame.display.flip()
