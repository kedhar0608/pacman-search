# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** CS3568 YOUR CODE HERE ***"
        "Decribe your function:"
        #  Mainly focusing on having the food. Do not go ahead when the ghost is over there.
        foodLocations=newFood.asList()
        minFoodDist=float("inf")
        score=successorGameState.getScore()
        for food in foodLocations:
            minFoodDist = min(minFoodDist,manhattanDistance(newPos, food))

        # neglect the ghost when its too close
        for ghost in successorGameState.getGhostPositions():
            # we avoid the ghost if the manhattan distance between current agent position and ghost positions is less than 1
            if (manhattanDistance(newPos, ghost) <1):
                return -float('inf')
        #returns the score
        return score + (1.0 /minFoodDist)

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** CS3568 YOUR CODE HERE ***"
        "PS. It is okay to define your own new functions. For example, value, min_function,max_function"

        def minimax(state, depth, agent):

            # if we find the bottom nodes or
            # if does not have any moves or
            # if we win or loose
            # Call evaluation function and return the result
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state), None

            negativeInfinity = float("-inf")
            maximiserValue = negativeInfinity
            no_of_agents=state.getNumAgents()

            # agent is pacman
            # Return the max value and the action
            if agent == 0:
                for action in state.getLegalActions(agent):
                    newState=state.generateSuccessor(agent, action)

                    (value, nextAction) = minimax(newState, depth, (agent + 1) % no_of_agents)
                    # Finding out the maximum value
                    if value > maximiserValue:
                        maximiserValue = value
                        maximiser_action= action
            if maximiserValue is not negativeInfinity:
                return maximiserValue, maximiser_action

            positiveInfinity = float("inf")
            minimiserValue = positiveInfinity
            # if the agent is ghost
            if agent !=0:
                for action in state.getLegalActions(agent):
                    newState = state.generateSuccessor(agent, action)
                    # keep the consistent depth if it is not the last ghost
                    if ((agent +1) % state.getNumAgents()) != 0:
                        (value, nextAction)= minimax(newState, depth, (agent + 1) % no_of_agents)
                    # else increment the depth by 1
                    else:
                        (value, nextAction) = minimax(state.generateSuccessor(agent, action), depth +1,
                                                              (agent + 1) % no_of_agents)
                    if value < minimiserValue:
                        minimiserValue = value
                        minimiserAction = action
             # Return the min value and the action
            if value is not positiveInfinity:
                return minimiserValue, minimiserAction

        ##########################################################
        return minimax(gameState, 0, 0)[1]
        # util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** CS3568 YOUR CODE HERE ***"
        "PS. It is okay to define your own new functions. For example, value, min_function,max_function"
        def alpha_beta(state, depth, agent, alpha, beta):

            # if we find the bottom nodes or
            # if does not have any moves or
            # if we win or loose
            # Call evaluation function and return the result
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state), None

            negativeInfinity = float("-inf")
            maximiserValue = negativeInfinity
            no_of_agents=state.getNumAgents()

            if agent == 0:
                for action in state.getLegalActions(agent):
                    newState=state.generateSuccessor(agent, action)

                    (value, nextAction) = alpha_beta(newState, depth, (agent + 1) % no_of_agents,alpha,beta)
                   
                    if value > maximiserValue:
                        maximiserValue = value
                        maximiser_action= action
                    if maximiserValue >beta:
                        return maximiserValue,maximiser_action
                    alpha=max(alpha,maximiserValue)
            if maximiserValue is not negativeInfinity:
                return maximiserValue, maximiser_action

            positiveInfinity = float("inf")
            minimiserValue = positiveInfinity
           
            if agent !=0:
                for action in state.getLegalActions(agent):
                    newState = state.generateSuccessor(agent, action)
                    # keep the consistent depth if it is not the last ghost
                    if ((agent +1) % state.getNumAgents()) != 0:
                        (value, nextAction)= alpha_beta(newState, depth, (agent + 1) % no_of_agents,alpha,beta)
                    # else increment the depth by 1
                    else:
                        (value, nextAction) = alpha_beta(state.generateSuccessor(agent, action), depth +1,
                                                              (agent + 1) % no_of_agents,alpha,beta)
                    if value < minimiserValue:
                        minimiserValue = value
                        minimiserAction = action
                    if  value <alpha :
                        return minimiserValue ,minimiserAction
                    beta= min(beta,minimiserValue)
                return minimiserValue,minimiserAction
             # Return the min value and the action
           

        return alpha_beta(gameState, 0, 0, float("-inf"), float("inf"))[1]
        util.raiseNotDefined()






class ExpectimaxAgent(MultiAgentSearchAgent):
    """
     Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** CS3568 YOUR CODE HERE ***"
        def expectimax(state, depth, agent):

            # if we find the bottom nodes or
            # if does not have any moves or
            # if we win or loose
            # Call evaluation function and return the result
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state), None

            negativeInfinity = float("-inf")
            maximiserValue = negativeInfinity
            no_of_agents=state.getNumAgents()

            # agent is pacman
            # Return the max value and the action
            if agent == 0:
                for action in state.getLegalActions(agent):
                    newState=state.generateSuccessor(agent, action)

                    (value, nextAction) = expectimax(newState, depth, (agent + 1) % no_of_agents)
                    # Finding out the maximum value
                    if value > maximiserValue:
                        maximiserValue = value
                        maximiser_action= action
            if maximiserValue is not negativeInfinity:
                return maximiserValue, maximiser_action

            positiveInfinity = float("inf")
            total=0.0
            count=0.0

            # if the agent is ghost
            if agent !=0:
                for action in state.getLegalActions(agent):
                    newState = state.generateSuccessor(agent, action)
                   
                    if ((agent +1) % state.getNumAgents()) != 0:
                        (value, nextAction)= expectimax(newState, depth, (agent + 1) % no_of_agents)
                    
                    else:
                        (value, nextAction) = expectimax(state.generateSuccessor(agent, action), depth +1,
                                                              (agent + 1) % no_of_agents)
                    total=total+value
                    count=count+1
                    minimiserAction=action

             # Return the average and the action
          
                return total/count, minimiserAction

        ##########################################################
        return expectimax(gameState, 0, 0)[1]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <we have given higher prefrence to eating scared ghosts when they are near and scared time is available. 
    In our scoring method we assigned 2 points for scared ghost and 1 point for food this score decreases with distance.So ,when the ghost is near and edible with scared time left
    we wncourage pacman to proceed in that state. If ghost is not edible we discourage with less evaulation score. Likewise for food we encourage it is nearer to pacman>
    """
    "*** CS3568 YOUR CODE HERE ***"
    score=currentGameState.getScore()
    for state in currentGameState.getGhostStates():
        distance=manhattanDistance(currentGameState.getPacmanPosition(),state.getPosition())
        if distance>0:
             if state.scaredTimer>0:
                score= score+2.0/distance
             else:
                score=score-1.0/distance
    "finding the manhattan distance between pacman and every other food location and inserting them into a list"
    food_locations_list=[]
    for food in currentGameState.getFood().asList():
        dis=manhattanDistance(currentGameState.getPacmanPosition(),food)
        food_locations_list.append(dis)
    
    if len(food_locations_list)!=0:
        score=score+1.0/min(food_locations_list)
    
    return score
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
