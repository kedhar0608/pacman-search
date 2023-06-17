import util

class DFS(object):
    def depthFirstSearch(self, problem):
        """
        Search the deepest nodes in the search tree first
        [2nd Edition: p 75, 3rd Edition: p 87]

        Your search algorithm needs to return a list of actions that reaches
        the goal.  Make sure to implement a graph search algorithm
        [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

        To get started, you might want to try some of these simple commands to
        understand the search problem that is being passed in:

        print "Start:", problem.getStartState()
        print "Is the start a goal?", problem.isGoalState(problem.getStartState())
        print "Start's successors:", problem.getSuccessors(problem.getStartState())
        """
        "*** TTU CS3568 YOUR CODE HERE ***"
        head=problem.getStartState() #saving starting state of the problem in head
        if problem.isGoalState(head): #checking if the start state is goal itself. If yes we return empty list of actions
            return []
        fringe=util.Stack()
        visitedStates=[]
        path=[]
        fringe.push((head,path))
        while fringe.isEmpty()==False:
            top=fringe.pop()
            currentState=top[0]
            actions=top[1]
            
            if currentState not in visitedStates: #prevents from visiting the same state again
                visitedStates.append(currentState)


                if problem.isGoalState(currentState)==True: #checks wheter current state is goalstate or not if yes returns set of actions till this state
                    return actions
                                          
                for  i in problem.getSuccessors(currentState): #reading successsor states and actions to reach them and storing them onto fringe
                    state = i[0]
                    action=i[1]
                    newPath=actions+[action]
                    nextState=(state,newPath)
                    fringe.push(nextState)
      
        util.raiseNotDefined()

class BFS(object):
    def breadthFirstSearch(self, problem):
        "*** TTU CS3568 YOUR CODE HERE ***"
        head=problem.getStartState() #saving starting state of the problem in head
        if problem.isGoalState(head): #checking if the start state is goal itself. If yes we return empty list of actions
            return []
        fringe=util.Queue()
        visitedStates=[]
        path=[]
        fringe.push((head,path))
        while fringe.isEmpty()==False:
            front=fringe.pop()
            currentState=front[0]
            actions=front[1]
            if problem.isGoalState(currentState): #checks wheter current state is goalstate or not if yes returns set of actions till this state
                return actions
            
            if currentState not in visitedStates:
                visitedStates.append(currentState)

                
                for  i in problem.getSuccessors(currentState): #reading successsor states and actions to reach them and storing them onto fringe
                    nextState = i[0]
                    action=i[1]
                    newPath=actions+[action]
                    fringe.push((nextState,newPath))
    
        
        util.raiseNotDefined()

class UCS(object):
    def uniformCostSearch(self, problem):
        "*** TTU CS3568 YOUR CODE HERE ***"
        head=problem.getStartState() #saving starting state of the problem in head
        if problem.isGoalState(head): #checking if the start state is goal itself. If yes we return empty list of actions
            return []
        fringe=util.PriorityQueue()
        visitedStates=[]
        path=[]
        priority=0
        fringe.push((head,priority,path),priority)
        while fringe.isEmpty()==False:
            currentState,cummCost,actions=fringe.pop()
            
            if currentState not in visitedStates:  #prevents from visiting the same state again
                visitedStates.append(currentState)

                if problem.isGoalState(currentState)==True: #checks wheter current state is goalstate or not if yes returns set of actions till this state
                    return actions
                
                for  i in problem.getSuccessors(currentState): #reading successsor states and actions to reach them and storing them onto fringe
                    nextState = i[0]
                    action=i[1]
                    cost=i[2]
                    newPath=actions+[action]
                    priority=cummCost+cost
                    fringe.push((nextState,priority,newPath),priority)

        util.raiseNotDefined()
        
class aSearch (object):
    def nullHeuristic( state, problem=None):
        """
        A heuristic function estimates the cost from the current state to the nearest goal in the provided SearchProblem.  This heuristic is trivial.
        """
        return 0
    def aStarSearch(self,problem, heuristic=nullHeuristic):
        "Search the node that has the lowest combined cost and heuristic first."
        "*** TTU CS3568 YOUR CODE HERE ***"
        head=problem.getStartState() #saving starting state of the problem in head
        if problem.isGoalState(head): #checking if the start state is goal itself. If yes we return empty list of actions
            return []
        fringe=util.PriorityQueue()
        visitedStates=[]
        path=[]
        fringe.push((head,0,path),0)
        while fringe.isEmpty()==False:
            dequeue=fringe.pop()
            currentState=dequeue[0]
            cummCost=dequeue[1]
            actions=dequeue[2]
            
            if currentState not in visitedStates:  #prevents from visiting the same state again
                visitedStates.append(currentState)

                if problem.isGoalState(currentState)==True: #checks wheter current state is goalstate or not if yes returns set of actions till this state
                    return actions
                
                for  i in problem.getSuccessors(currentState): #reading successsor states and actions to reach them and storing them onto fringe
                    nextState = i[0]
                    action=i[1]
                    cost=i[2]
                    newPath=actions+[action]
                    newCost=cummCost+cost
                    heuristics=newCost+heuristic(nextState,problem)
                    fringe.push((nextState,newCost,newPath),heuristics)
        
        
        util.raiseNotDefined()

