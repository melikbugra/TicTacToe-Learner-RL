import pygame
import os
from grid import Grid
import numpy as np
import copy
from environment import QLearningEnv
from qlearningagent import QLearningAgent
import pickle

os.environ['SDL_VIDEO_WINDOW_POS'] = '600,200'

surface = pygame.display.set_mode((600, 600))
pygame.display.set_caption('TicTacToe')

grid = Grid()
a = [[]]
running = True
player = 'X'
with open("states.txt", "rb") as fp:
    states = pickle.load(fp)


eps = 0.01
step = 0.1
disc = 0.9
agentInfo = [9, eps, step, disc, 0]
currentState = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
env = QLearningEnv(states.index([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
qAgent = QLearningAgent(agentInfo)
with open("qMatrix.txt", "rb") as fp:
    qAgent.q = pickle.load(fp)

def agentPlay(rew, stt):
    act = qAgent.agent_step(rew, stt)

    x = int(act % 3)
    y = int((act - x) / 3)

    bools = grid.get_cell_value(x, y) == 'X' or grid.get_cell_value(x, y) == 'O'
    while bools:
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
        act = qAgent.agent_start(stt)

        x = int(act % 3)
        y = int((act - x) / 3)
        bools = grid.get_cell_value(x, y) == 'X' or grid.get_cell_value(x, y) == 'O'

    grid.set_cell_value(x, y, 'O')

    return act

first_time = True
with open("iteration.txt", "rb") as fp:
    iteration = pickle.load(fp)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x and first_time:
                states = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
                with open("states.txt", "wb") as fp:
                    pickle.dump(states, fp)
                q = np.zeros((1, 9))
                with open("qMatrix.txt", "wb") as fp:
                    pickle.dump(q, fp)
                iteration = 0
                with open("iteration.txt", "wb") as fp:
                    pickle.dump(iteration, fp)

        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            if pygame.mouse.get_pressed()[0] == 1:
                position = pygame.mouse.get_pos()
                cellIsFull = grid.get_cell_value(position[0] // 200, position[1] // 200) == 'O' or grid.get_cell_value(position[0] // 200, position[1] // 200) == 'X'
                grid.get_mouse(position[0] // 200, position[1] // 200,
                              player)# Piksellerden matris pozisoyn bilgisine geçiş
                # grid.check_grid(position[0] // 200, position[1] // 200, player)
                grid.switch_player = True
                if cellIsFull:
                    grid.switch_player = False
                if grid.switch_player:
                    if player == 'X':
                        player = 'O'
                    else:
                        player = 'X'

                currentState = copy.deepcopy(grid.grid)

                if currentState not in states:
                    qAgent.q = np.vstack((qAgent.q, [0, 0, 0, 0, 0, 0, 0, 0, 0]))
                    states.append(currentState)

                xxx = grid.draws

                if (grid.game_over and (grid.oWins or not grid.draws) and not grid.xWins) or first_time:
                    stt = env.getStateNum(states.index(currentState))
                    act = agentStart(stt)
                    rew = env.env_step()[0]
                    grid.switchPlayer = True
                    if grid.switch_player:
                        if player == 'X':
                            player = 'O'
                        else:
                            player = 'X'
                    grid.game_over = False
                    first_time = False

                # iteration += 1
                if (not grid.game_over and not grid.draws) and player == 'O':
                    currentState = copy.deepcopy(grid.grid)
                    if currentState not in states:
                        qAgent.q = np.vstack((qAgent.q, [0, 0, 0, 0, 0, 0, 0, 0, 0]))
                        states.append(currentState)
                        with open("qMatrix.txt", "wb") as fp:
                            pickle.dump(qAgent.q, fp)
                        states.append(currentState)
                        with open("states.txt", "wb") as fp:
                            pickle.dump(states, fp)
                    env = QLearningEnv(states.index(currentState))
                    stt = env.getStateNum(states.index(currentState))
                    act = agentPlay(rew, stt)
                    rew = env.env_step()[0]
                    print('\n', qAgent.q[stt], stt)
                    print('\n', currentState, '    no= ', states.index(currentState))

                    # print('\n', qAgent.q)
                    print('act= ', act)
                    print('stt= ', stt)
                    with open("qMatrix.txt", "wb") as fp:
                        pickle.dump(qAgent.q, fp)
                    with open("states.txt", "wb") as fp:
                        pickle.dump(states, fp)
                    print('rew', rew)

                    if grid.switch_player:
                        if player == 'X':
                            player = 'O'
                        else:
                            player = 'X'

            if grid.game_over:
                iteration += 1
                if iteration == 0:
                    iteration+=1
                iter_no = str(iteration)
                caption_str = 'Yineleme: ' + iter_no
                pygame.display.set_caption(caption_str)
                print(iteration)
                rew = env.env_end(grid.oWins)[0]
                print('Prev', qAgent.prev_action)
                qAgent.agent_end(rew)
                print('rew', rew)
                with open("iteration.txt", "wb") as fp:
                    pickle.dump(iteration, fp)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                with open("qMatrix.txt", "wb") as fp:
                    pickle.dump(qAgent.q, fp)
                with open("states.txt", "wb") as fp:
                    pickle.dump(states, fp)
                grid.clear_grid()
                grid.game_over = False
                grid.switch_player = False
                player = 'X'
            elif event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_x and grid.game_over:
                states = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
                with open("states.txt", "wb") as fp:
                    pickle.dump(states, fp)
                q = np.zeros((1, 9))
                with open("qMatrix.txt", "wb") as fp:
                    pickle.dump(q, fp)
                iteration = 0
                with open("iteration.txt", "wb") as fp:
                    pickle.dump(iteration, fp)
                grid.clear_grid()
                grid.game_over = False
                grid.switch_player = False
                player = 'X'

    surface.fill((0, 0, 0))

    grid.draw(surface)

    pygame.display.flip()
