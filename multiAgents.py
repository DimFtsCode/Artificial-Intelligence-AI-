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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        
        "*** YOUR CODE HERE ***"
        #Score of the state successor
        score = successorGameState.getScore()
        
        #List for distances from the succesor state to the ghost
        ghostDistances = []
        
        #List for distances from the succesor state to the food
        
        foodDistances = []
        
        foods = newFood.asList()
        
        #Append the manhattandistance of the succesor state via ghosts position in the list
        for x in newGhostStates:
          ghostDistances.append(manhattanDistance(newPos, x.getPosition()))
            
        #Append the manhattanDistance of the succesor state via food position in the list
        for x in foods: 
          foodDistances.append(manhattanDistance(newPos, x))
        MinGhostDistance = 0
        eq = 1
        #Ghosts distances not empty
        if len(newGhostStates) is not 0:
          MinGHostDistance = min(ghostDistances)    
          if MinGHostDistance == 1:
            eq = -1
          elif MinGHostDistance == 2:
            eq = -3
          elif MinGhostDistance > 3:
            eq = MinGHostDistance
          score += 30 / eq 


          
        #Foods distances not empty
        if len(foodDistances) is not 0 :
            eq = min(foodDistances)
            score += 10 / eq
        
        
        return score 

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        "*** YOUR CODE HERE ***"
        #pacman is maximizer and ghosts are minimizer 
        #because we want best movements for pacman we start calling the minimizer function 
        actions = []
        NextStates = []
        scores = []
        bestInd = []
        actions = gameState.getLegalActions(0) #legal actions for pacman
        NextStates = [ gameState.generateSuccessor(0,action) for action in actions ] #Next states for pacman(for every action one state)
            
        scores = [self.minimizer(0 , state , 1) for state in NextStates] #Scores usings the minimizer function for different pacman's states.
            
        best = max(scores) #finding the best scores   
           
        bestInd = [index for index in range(len(scores)) if scores[index] == best ] #finding the indexes for the best scores
                
        return actions[bestInd[0]] # because for 1 action  = 1 state and for 1 state is 1 score we can return the first best index as the best move.
        
        
        
    def maximizer(self, currentDepth , gameState):
        if self.depth == currentDepth or gameState.isLose() or gameState.isWin():# End state
            return self.evaluationFunction(gameState)
        else:# If not end state return the max for ghost no1 for all the differents states for all the differents moves that pacman can make.
            return max([self.minimizer(currentDepth, state , 1) for state in [gameState.generateSuccessor(0 , move ) for move in gameState.getLegalActions(0)]])
            
    def minimizer(self , currentDepth,gameState , ghostIndex ):
        if self.depth == currentDepth or gameState.isLose() or gameState.isWin():# End state
            return self.evaluationFunction(gameState)
        elif ghostIndex + 1 >= gameState.getNumAgents():# if we have search all the ghosts so we return min  maximizer for the depth + 1 for the same ghost 
            return min([self.maximizer(currentDepth + 1, state) for state in [gameState.generateSuccessor(ghostIndex , move ) for move in gameState.getLegalActions(ghostIndex)]])
        elif ghostIndex +1 < gameState.getNumAgents(): # we want min minimizer for the next ghost.
            return min([self.minimizer(currentDepth, state ,ghostIndex + 1) for state in [gameState.generateSuccessor(ghostIndex, move ) for move in gameState.getLegalActions(ghostIndex)]])
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        def alpha_beta(state, agent, depth, Alpha, Beta):
            
       
            if depth == self.depth or state.getLegalActions(agent) == 0 or state.isWin() or state.isLose():            
                return (self.evaluationFunction(state), None)
                
            minimum = float("-inf")
            val = minimum
            if (agent is 0): #Max situation agent = pacman
                for action in state.getLegalActions(agent): 
                    successor = state.generateSuccessor(agent, action) #find the successor
                    (v, action1) = alpha_beta(successor, (agent + 1) % state.getNumAgents(),depth, Alpha, Beta)
                    if(v > val): #finding the max of all the values
                        val = v
                        maxa = action
                    if val > Beta: 
                        return (val, maxa)
                    Alpha = max(Alpha, val)         
            
            #return the max value - action
            if val is not minimum:
                return (val, maxa)  
 
            maximum = float("inf")
            val1 = maximum 
            if (agent is not 0): #Min situation agent =  ghost
                for action in state.getLegalActions(agent): #for all the actions
                    successor = state.generateSuccessor(agent, action) #find the successor
                    if(((agent + 1) % state.getNumAgents()) is not 0): #if is not the last agent go to the next
                        (v, action1) = alpha_beta(successor, (agent + 1) % state.getNumAgents(), depth, Alpha, Beta)
                    else: #if it is the last agent go to the next depth
                        (v, action1) = alpha_beta(successor, (agent + 1) % state.getNumAgents(), depth + 1, Alpha, Beta)
                    if(v < val1): #finding the min of all the values
                        val1 = v
                        mina = action
                    if val1 < Alpha:
                        return (val1, mina)
                    Beta = min(Beta, val1)
            #returns the min value - action           
            if val1 is not maximum:
                return (val1, mina)
        
        return alpha_beta(gameState, 0, 0,  float("-inf"),float("inf"))[1] #is calling the function and returns the actions only
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
        "*** YOUR CODE HERE ***"
        def expectimax(state, agent, depth):
            
            
            if depth == self.depth or state.getLegalActions(agent) == 0 or state.isWin() or state.isLose():            
                return (self.evaluationFunction(state), None)
                
            minimum = float("-inf")
            val = minimum
            if (agent is 0): #Max situation agent = pacman
                for action in state.getLegalActions(agent): 
                    successor = state.generateSuccessor(agent, action) #find the successor
                    (v, action1) = expectimax(successor, (agent + 1) % state.getNumAgents(),depth)
                    if(v > val): #finding the max of all the values
                        val = v
                        maxa = action
            #return he max value - action
            if val is not minimum:
                return (val, maxa)  
            maximum = float("inf")
            val1 = 0.0
            counter = 0.0
            if (agent is not 0): #Min situation agent =  ghost
                for action in state.getLegalActions(agent): #for all the actions
                    successor = state.generateSuccessor(agent, action) #find the successor
                    if(((agent + 1) % state.getNumAgents()) is not 0): #if is not the last agent go to the next
                        (v, action1) = expectimax(successor, (agent + 1) % state.getNumAgents(), depth)
                    else: #if it is the last agent go to the next depth
                        (v, action1) = expectimax(successor, (agent + 1) % state.getNumAgents(), depth + 1)
                    val1+=v  # the sum of the values
                    counter +=1 # the number of the counters
                    mina = action # a random choise
            #returns the min value - action           
            if val1 is not maximum:
                return (val1/counter, mina)
        
        return expectimax(gameState, 0, 0)[1] #is calling the function and returns the actions only
   
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    
    score = currentGameState.getScore()
    
    ghostValue = 30.0   
    foodValue = 10.0
    scaredGhostValue = 50.0  #bigger value for the scared ghost because we want to prefer it as a move     
    eq = 1.0
    #For every ghost
    for x in newGhostStates:
        #Find the distance from pacman
        dis = manhattanDistance(newPos, x.getPosition())
        if dis > 0:
            
            
            if x.scaredTimer > 0: #if it is scare ghost
                score += scaredGhostValue / dis #its a good situation we want it 
            else:
                if dis == 1: #for dis = 1 the ghost is close and we dont want such situatior
                    eq = -0.3 #so we substrack a bigger persentage of total ghost value
                elif dis == 2: #same logic if the dis = 2
                    eq = -0.1 # but with smaller persentage
                elif dis > 3: # we want situations that dis is > 3 the ghost is away
                    eq = dis
                score += ghostValue / eq # So we add to the score 
            

    #Find the distance of every food and insert it in a list using manhattan
    foodList = newFood.asList()
    foodDistances = []
    
    for x in foodList: 
        foodDistances.append(manhattanDistance(newPos, x))

    #If there is at least one food
    if len(foodDistances) is not 0: 
        score += foodValue / min(foodDistances) # we need the smallest food for out new position
    
    #Return the final Score
    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
