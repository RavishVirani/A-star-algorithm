import random
from queue import PriorityQueue # I read the documentation. Implements a heap under the hood
import copy

def disorder(state):
    #If two states have the same parity of disorder, they can reach each other
    total = 0
    for i in range(len(state)):
        for n in range(i+1,len(state)):
            if state[i]>state[n] and state[i]!=0 and state[n]!=0:
                total+=1
    return total

def possible(state,position,width):
    #Assume that the second state is the goal state 1,..,n,0
    if width%2 ==1:
        return disorder(state)%2 == 0
    else:
        y = position//width
        inversion = disorder(state)%2
        if y%2==0 and inversion==1:
            return True
        elif y%2==1 and inversion==0:
            return True
        return False

def match(state1,state2):
    if len(state1) == len(state2):
        for i in range(len(state1)):
            if state1[i]!=state2[i]:
                return False
        return True
    return False

def createRandom(n):
    #n = length of list
    state = [0]*n
    temp = [0]*n
    num=0
    repeated = True
    position = -1
    for i in range(n):
        while repeated:
            num = random.randint(0,n-1)
            if temp[num]==0:
                state[i]=num
                repeated = False
                temp[num]=1
                if num ==0:
                    position = i
        repeated = True
    return state,position

def opposite(direct):
    if direct ==1:
        return 2
    elif direct==2:
        return 1
    elif direct ==3:
        return 4
    elif direct ==4:
        return 3
    return 0

def swap(state,pos,n,direct):
    #1234URDL
    x = pos%n
    y = pos//n
    new_state = copy.deepcopy(state)
    if direct == 1:
        if y!=0:
            temp = new_state[pos - n]
            new_state[pos-n] = 0
            new_state[pos] = temp
            return new_state, pos - n
    elif direct ==4:
        if x!=n-1:
            temp = new_state[pos + 1]
            new_state[pos + 1] = 0
            new_state[pos] = temp
            return new_state , pos + 1
    elif direct ==2:
        if y!=n-1:
            temp = new_state[pos + n]
            new_state[pos + n] = 0
            new_state[pos] = temp
            return new_state, pos + n  
    else:
        if x!=0:
            temp = new_state[pos - 1]
            new_state[pos - 1] = 0
            new_state[pos] = temp
            return new_state, pos - 1
    return None,None

def bfs(state1,state2,n):
    return 0

def misplaced_tiles(state1, state2, n):
    h = 0

    for i in range(n*n):
        if state1[i] != 0 and state1[i] != state2[i]:
            h += 1
    
    return h

def misplaced_positions(state1, state2, n):
    h = 0
    row1 = [1,2,3]
    row2 = [4,5,6]
    row3 = [7,8,0]
    col1 = [1,4,7]
    col2 = [2,5,8]
    col3 = [3,6,0]
    
    if (state1[0] not in row1):
        h+=1
    if (state1[0] not in col1):
        h+=1
    if (state1[1] not in row1):
        h+=1
    if (state1[1] not in col2):
        h+=1
    if (state1[2] not in row1):
        h+=1
    if (state1[2] not in col3):
        h+=1
    if (state1[3] not in row2):
        h+=1
    if (state1[3] not in col1):
        h+=1
    if (state1[4] not in row2):
        h+=1
    if (state1[4] not in col2):
        h+=1
    if (state1[5] not in row2):
        h+=1
    if (state1[5] not in col3):
        h+=1
    if (state1[6] not in row3):
        h+=1
    if (state1[6] not in col1):
        h+=1
    if (state1[7] not in row3):
        h+=1
    if (state1[7] not in col2):
        h+=1
    if (state1[8] not in row3):
        h+=1
    if (state1[8] not in col3):
        h+=1

    return h

def makeNode(current_node,goal_state,queue,heuristic,direct,q,SIZE,visited):
    if opposite(current_node)!=direct:
        temp_state, pos = swap(current_node.state,current_node.position,SIZE,direct)
        #Need pos to be the new position of the 0 tile
        if temp_state != None and temp_state not in visited:
            temp_node = Node(temp_state,current_node.totalCost+1,pos)
            h = heuristic(temp_node.state, goal_state,SIZE)
            temp_node.parent = direct
            #Heuristic applied only on the tile moved
            #weight = current_node.hCost - ONE_FUNCTION(current_node.state,goal_state,SIZE,pos) + ONE_FUNCTION(temp_state,goal_state,SIZE,current_node.position)
            #temp_node.hCost = weight

            #Each Queue item is (F(n) , Order put in, node)
            #queue.put((temp_node.totalCost + h,10000000000-q,temp_node)) # This is LIFO
            queue.put((temp_node.totalCost + h,q,temp_node)) # This is FIFO        
            q+=1
    return q


class Node:
    state = None
    #parent #needed? can be nice to visualize
    totalCost = None #Cost so far 
    parent = None
    position = None # position of the blank so swapping will be slightly faster
    hCost = None # current heuristic cost. Could be cheaper to keep updating heuristic costs rather than recomputing them
    def __init__(self,state,totalCost,pos):
        self.state = state
        self.totalCost = totalCost
        self.position = pos
    def display(self,n):
        for i in range(n):
            for q in range(n):
                print(self.state[i*n+q],end = " ")
            print()
    def __eq__(self,other):
        return self.state == other
SIZE = 3 # the side length of the puzzle. n where n creates an nxn puzzle

goal_state = list(range(1,SIZE*SIZE))

goal_state.append(0)
print(goal_state)

searching = PriorityQueue()
visited = []

current_node = None
solutionCost = []
nodeCost = []
q = 0 #Insertion order
used = []

#FUNCTION = bfs
#FUNCTION = manhattan
FUNCTION = misplaced_tiles
# FUNCTION = misplaced_positions

#TIME ISSUE Look for inefficiencies or translate to faster language?
#Same 100 boards for the heuristics or different? Should we also guarantee distinct patterns?

for i in range(100):
    #Create the random starting state
    while True:
        current_state,pos = createRandom(SIZE*SIZE)
        if possible(current_state,pos,SIZE) and current_state not in used: # the disorder of goal is even
            used.append(current_state): # the disorder of goal is even

            #Test Puzzles
            #current_state = [5,2,11,9,3,15,8,6,14,10,1,7,4,0,13,12]
            #pos = 13
            #current_state = [4,8,2,7,0,6,5,3,1]
            #pos = 4
            
            current_node = Node(current_state,0,pos)
            current_node.hCost = FUNCTION(current_state, goal_state,SIZE)
            current_node.display(SIZE)
            break
        
    visited = []# Can the visited states be put in something more efficient to look through
    #Maybe a hash table with the starting integer as the key?
    searching = PriorityQueue()
    num_node = 0    

    while not match(current_node.state,goal_state): # Should not be an infinite loop due to disorder check
        #Add each children to the priority Queue
        q=makeNode(current_node,goal_state,searching,FUNCTION,1,q,SIZE,visited) # UP
        q=makeNode(current_node,goal_state,searching,FUNCTION,2,q,SIZE,visited) # Right
        q=makeNode(current_node,goal_state,searching,FUNCTION,3,q,SIZE,visited) # Down
        q=makeNode(current_node,goal_state,searching,FUNCTION,4,q,SIZE,visited) # Left

        #Add current node as one that is already visited
        visited.append(current_node.state)
        num_node += 1

        #Take the next node that has the smallest value
        current_node = searching.get()[2]
        
    print("FINISHED PUZZLE NUBMER {}".format(i))
    solutionCost.append(current_node.totalCost)
    nodeCost.append(num_node)

print(solutionCost)
print(nodeCost)
