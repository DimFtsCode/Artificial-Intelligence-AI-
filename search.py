# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    start = problem.getStartState()#initiate start point
    visited = set()#initiate set
    states = util.Stack()#initate stack
    tuple = (start , [] )# create a tuple of start and a list
    states.push(tuple)#push tuple in stack
    while not states.isEmpty():# if stack not empty
        state,moves = states.pop()
        visited.add(state)
        if problem.isGoalState(state):#if problem is a goal return moves
            return moves
        successors = problem.getSuccessors(state)#the succesors of state
        for i in successors:
            c = i[0]
            if c not in visited:#if succesors not visited
                temp = i[0]
                direction = i[1]
                tuple1 = (temp, moves + [direction])
                states.push(tuple1)
    return moves + [direction]#return moves + last directions
    
    
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    """the only different with dfs is that in bfs we use queue and not stack. With that way we remove the first element inside queue set"""
    start = problem.getStartState()
    visited = set()
    visited.add(start)
    states = util.Queue()
    tuple = (start, [])
    states.push(tuple)
    while not states.isEmpty() :
        
        state , moves = states.pop()
        if problem.isGoalState(state):
            return moves
        visited.add(state)
        successors = problem.getSuccessors(state)
        for i in successors:
            c = i[0]
            if not c in visited:
            
                direction = i[1]
                visited.add(c)
                tuple = (c , moves + [direction])
                states.push(tuple)
    return moves + [direction] 
        
        
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    """ IN UCS we use priorityQueue and not stack or queue. In that way we remove for fringe the element with the smallest cost"""
    start = problem.getStartState()
    tuple = (start , [])
    visited = set()
    states = util.PriorityQueue()
    states.push(tuple , 0)
    while not states.isEmpty(): 
        state , moves = states.pop()
        if problem.isGoalState(state):
            return moves 
        if not state in visited :
            succ = problem.getSuccessors(state)
            for s in succ:
                cp = s[0]
                if not cp in visited:
                    direction = s[1]
                    steps = moves + [direction]
                    newcost = problem.getCostOfActions(steps)
                    tuple = ( cp,steps )
                    states.push(tuple , newcost)
        visited.add(state)
    return moves + [direction]
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    """The diffest in a* is that everytime we put in PriorityQueue the element with the smallest cost + heuristic cost"""
    start = problem.getStartState()
    tuple = (start , [])
    visited = set()
    states = util.PriorityQueue()
    states.push(tuple , heuristic(start, problem))
    newcost = 0 
    while not states.isEmpty(): 
        state , moves = states.pop()
        if problem.isGoalState(state):
            return moves 
        if not state in visited :
            succ = problem.getSuccessors(state)
            for s in succ:
                cp = s[0]
                if not cp in visited:
                    direction = s[1]
                    steps = moves + [direction]
                    newcost = problem.getCostOfActions(steps) + heuristic(cp, problem)
                    tuple = ( cp , steps )
                    states.push(tuple , newcost)
        visited.add(state)
    return moves + [direction]
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
