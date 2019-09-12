# import sys
# sys.path.append('../../')
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__)))))
from main.Maze import Maze
from main.Agent import Agent
from main.mysolution.MyQLearning import MyQLearning
from main.mysolution.MyEGreedy import MyEGreedy
import matplotlib as plt
from matplotlib import pyplot
if __name__ == "__main__":
    # load the maze
    # TODO replace this with the location to your maze on your file system

    # toy maze
    file = "..\\..\\data\\toy_maze.txt"
   

    # easy maze
    # file = "..\\..\\data\\easy_maze.txt"
    # endx = 24
    # endy = 14

    maze = Maze(file)
    endy = len(maze.states) - 1
    endx = len(maze.states[0]) - 1
    # Set the reward at the bottom right to 10
    maze.set_reward(maze.get_state(endx, endy), 100)
    maze.set_reward(maze.get_state(9, 0), 50)
    print(f'{endx}, {endy}')

    # maze.set_reward(maze.get_state(9, 3), 10)
    # create a robot at starting and reset location (0,0) (top left)
    robot = Agent(0, 0)

    # make a selection object (you need to implement the methods in this class)
    selection = MyEGreedy()

    # make a Qlearning object (you need to implement the methods in this class)
    learn = MyQLearning()

    stop = False
    original_eps = 0.4
    epsilon = original_eps
    alpha = 0.7
    gamma = 0.9

    a = 0.05  # minus if at correct location
    b = 0.05  # plus if at wrong location

    totalactions = 0
    average = 0
    runs = 0
    mean = []
    gem = []
    goalsreached = []
    goalsteps = []
    temptationsteps = []
    last10 = []
    steps = 100
    meanruns = 9
    limit = 3000000
    stepstaken = []
    # keep learning until you decide to stop
    for i in range(meanruns):
        while not stop:
            # we increment the totalactions
            totalactions += 1
            # we get our next action
            curstate = robot.get_state(maze)
            possibleactions = maze.get_valid_actions(robot)

            nextaction = selection.get_egreedy_action(
                robot, maze, learn, epsilon)

            # we take our next action
            robot.do_action(nextaction, maze)
            nextstate = robot.get_state(maze)
            nextpossible = maze.get_valid_actions(robot)
            # we get our reward
            reward = maze.get_reward(robot.get_state(maze))
            # update the Q
            learn.update_q(state=curstate, action=nextaction, r=reward,
                           state_next=nextstate, possible_actions=nextpossible, alpha=alpha, gamma=gamma)
            if robot.x == endx and robot.y == endy:
                stepstaken.append(robot.nr_of_actions_since_reset)
                goalsteps.append(robot.nr_of_actions_since_reset)
                runs += 1
                goalsreached.append(1)
                if epsilon >= a:
                    epsilon -= a
                    # epsilon -= 0.005
                    if epsilon < 0:
                        epsilon = 0
                if len(stepstaken) + 10 >= steps:
                    last10.append(1)

                # print("reached goal, resetting...")
                robot.reset()
                if len(stepstaken) > steps:
                    average = sum(stepstaken) / steps
                    stepstaken = []
                    mean.append(average)
                    break

            if robot.x == 9 and robot.y == 0:
                stepstaken.append(robot.nr_of_actions_since_reset)
                goalsteps.append(-robot.nr_of_actions_since_reset)
                runs += 1
                goalsreached.append(2)
                if epsilon > 0 and epsilon < 1-b:
                    epsilon += b
                    pass
                if len(stepstaken) + 10 >= steps:
                    last10.append(2)
                # print("reached goal, resetting...")
                robot.reset()
                if len(stepstaken) > steps:

                    average = sum(stepstaken) / steps
                    stepstaken = []
                    mean.append(average)
                    break

            if totalactions >= limit:
                print(f"Exceeded limit of {limit:,} steps, quitting...")
                print("robot was busy with ")
                ave = sum(stepstaken) / runs
                stepstaken = []
                mean.append(ave)
                runs = 0
                robot.reset()
                stop = True
        epsilon = original_eps
        learn = MyQLearning()
        totalactions = 0
        i += 1
        stop = False
    gem.append(mean)
    mean = []

    print(gem)
    middel = []
    for l in range(len(gem)):
        middel.append(sum(gem[l])/len(gem[l]))
    print(middel)
    print(
        f"Over all {len(goalsreached)} iteration we went to the exit {100*goalsreached.count(1)/len(goalsreached):.2f}% of the time,\nand to the temptation {100*goalsreached.count(2)/len(goalsreached):.2f}% of the time.")
    print(
        f"The last 10 iterations before resetting QLearning went to the exit {100*last10.count(1)/len(last10):.2f}% of the time,\nand to the temptation {100*last10.count(2)/len(last10):.2f}% of the time.")

    goalsteps2 = goalsteps.copy()
    for i,s in enumerate(goalsteps):
        if s <= 0:
            goalsteps[i] = None
    for i,s in enumerate(goalsteps2):
        if s > 0:
            goalsteps2[i] = None

    xposition = range(0, 900, 100)
    for xc in xposition:
        pyplot.axvline(x=xc, color='k', linestyle='--')
    pyplot.scatter(range(len(goalsteps)),goalsteps, color='g', marker='.')
    pyplot.scatter(range(len(goalsteps)),goalsteps2, color='r', marker='.')
    pyplot.ylabel("Steps taken to completion (negative means wrong goal)")
    pyplot.xlabel("Iteration")
    pyplot.show()
