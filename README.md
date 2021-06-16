# TicTacToe-Learner-RL
A TicTacToe AI (Reinforcement Learning) player agent that learns to play 'O' player in the game from the user agent who plays 'X' agent. Also another program is added: In this program 'X' player is also a AI agent and both AI's learns from each other, so we can use their knowledge in our first program and test them.

In this study, TicTacToe game algorithm and its image resources are taken from AtiByte YouTube channel and here is the link for the reference: https://www.youtube.com/watch?v=K14vOZjHNLA&list=PL1P11yPQAo7pJT26yr1_cmfS1g_RX7b4d

I used this resource's code and added AI agents on it.

### Explanations
1. LearnsFromUser
* LearnsFromUser folder contains the program that an RL agent learns how to play TicTacToe from you. It plays against you at the start with no knowledge about the game. It plays randomly. As it plays, it learns how to play the game with real experience, like a baby!
* In res folder, there are the image assets of 'X' and 'O' players.
* In environment.py, TicTacToe game is defined as a RL environment. It contains QLearningEnv class.
* qlearningagent.py contains the QLearningAgent class.
* game.py and grid.py contains the codes for game mechanics of TicTacToe created with pygame package. game.py is the main program.
* iteration.txt holds the iteration number and states.txt and qMatrix.txt are the memory of the agent.

You can use the 'X' key to reset the AI's memory.
You can only use the reset option if you have just opened the game or completed a chapter.
When the game is over, you can use the 'SPACE' key to start the new game.
The artificial intelligence will completely learn from you and develop strategies against your strategies.
Unless you reset his memory, it will never forget what it has learned.

2. LearnsFromEachOther
In this program 2 AIs learn from each other. You can run this program to train them. When you decide that training is enough, you can use memory txt files for the first program and test them against you.


![image](https://user-images.githubusercontent.com/68668304/122187269-916aa100-ce97-11eb-947c-53c402acd4e2.png)
