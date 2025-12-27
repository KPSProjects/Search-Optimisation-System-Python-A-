#aips informed search library
#By K. Hui

import aips.search as search
import math

#best-first search is a subclass of search problem
class BestFirstSearchProblem(search.SearchProblem):
    goalState=None                  #most best-first search need a goal to compute f(n)
    
    #constructor
    #we assume there is an initial and goal states
    def __init__(self,start,goal):
        super().__init__(start)
        self.goalState=goal

    #best-first search
    def search(self):
        visitedNodes={} #create empty history map
        fringe=[]       #empty fringe list
        rootNode=search.Node(self.startState,None,None)    #create root node
        fringe.append(rootNode)                     #add root node into fringe
        
        visitedNodes[rootNode.state]=rootNode       #put state-node pair into visited node map
        self.nodeVisited+=1                         #increment visited node count

        if self.nodeVisited%1000==0:
            print("No. of nodes explored: {}\n".format(self.nodeVisited))   #print message every 1000 nodes

        while True:
            if fringe==[]:  #fringe is empty
                return None #no solution
            
            node=fringe.pop(0)                      #remove 1st node from fringe list
            if self.isGoal(node.state):             #goal state found
                return self.constructPath(node)     #construct path and return

            successors=node.state.successor()  #get all successors
            for child in successors:
                self.nodeVisited+=1
                if self.nodeVisited%1000==0:
                    print("No. of nodes explored: {}\n".format(self.nodeVisited))   #print message every 1000 nodes
                action=child.action     #get action from action-state pair
                nextState=child.state   #get next state from action-state pair
                lastSeenNode=visitedNodes.get(nextState)    #look up next state from history map
                if lastSeenNode==None:  #have not seen this state before
                    childNode=search.Node(nextState,node,action)   #create child node from state
                    self.addChildBinary(fringe,childNode)                 #add child into fringe
                    visitedNodes[nextState]=childNode               #add next state and childnode pair into history map
                else:
                    if lastSeenNode.getCost()>action.cost+node.getCost():    #this new path is cheaper
                        lastSeenNode.parent=node    #go through the current node to reach this next state
                        lastSeenNode.action=action  #update action too

    #add new node into fringe using linear search based on f(n) value
    def addChildLinear(self,fringe,childNode):
        for i in range(0,len(fringe)):              #scan fringe list
            if self.evaluation(childNode)<self.evaluation(fringe[i]): #find position where node is just bigger than child in evaluation function value
                fringe.insert(i,childNode)      #add child just before that node
                return                          #exit, no need to continue
        fringe.append(childNode)    #if you hit the end of list, add child to the end
    
    #add new node into fringe using binary search based on f(n) value
    def addChildBinary(self,fringe,childNode):
        self.binaryInsert(fringe,childNode,0,len(fringe)-1) #insert node into fringe using binary insertion
    
    def binaryInsert(self,fringe,node,left=None,right=None):
        if left==None:
            left=0
        if right==None:
            right=len(fringe)-1
    
        while True:        
            if left>right:
                fringe.insert(left,node)
                return

            nodeValue=self.evaluation(node)                     #f(n) value of new node   
            if left==right:                                     #left meets right
                leftValue=self.evaluation(fringe[left])         #f(n) of node at position left
                if leftValue>nodeValue:         #new node goes before left
                    fringe.insert(left,node)
                    return
                elif leftValue==nodeValue:      #new node goes before left
                    if fringe[left].getCost()>node.getCost():   #g(n) of new node is lower, thus less certain
                        fringe.insert(left+1,node)              #new node goes after old node
                        return
                    fringe.insert(left,node)                    #otherwise new node goes before old node
                    return
                else:
                    fringe.insert(left+1,node)   #value goes after left
                    return
            #has at least 2 elements in range
            else:    
                mid=math.floor((left+right)/2)          #find middle position
                midValue=self.evaluation(fringe[mid])   #find f(n) value of node at position mid
                if midValue==nodeValue:                 #the same f(n) value
                    if fringe[mid].getCost()>node.getCost():    #g(n) of new node is lower, thus less certain
                        fringe.insert(mid+1,node)               #new node goes after old node
                        return
                    fringe.insert(mid,node)             #otherwise new node goes before mid
                    return
                if midValue>nodeValue:                  #new node go into the segment before mid
                    right=mid-1
                else:
                    left=mid+1

    #evaluation to be defined in the concrete search problem    
    def evaluation(self,node):
        pass
