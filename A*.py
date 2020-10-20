import random
from queue import PriorityQueue
import copy

def disorder(state):
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

def manhattan(state1, state2, n):
    res = 0
    for i in range(n*n):
        if state1[i] != 0 and state1[i] != state2[i]:
            ci = state2.index(state1[i])
            y = (i // n) - (ci // n)
            x = (i % n) - (ci % n)
            res += abs(y) + abs(x)
    return res

def linear_conflicts(state1, state2, n):

    def count_conflicts(state1_row, state2_row, n, ans=0):
        counts = [0 for x in range(n)]
        for i, tile_1 in enumerate(state1_row):
            if tile_1 in state2_row and tile_1 != 0:
                for j, tile_2 in enumerate(state1_row):
                    if tile_2 in state2_row and tile_2 != 0:
                        if tile_1 != tile_2:
                            if (state2_row.index(tile_1) > state2_row.index(tile_2)) and i < j:
                                counts[i] += 1
                            if (state2_row.index(tile_1) < state2_row.index(tile_2)) and i > j:
                                counts[i] += 1
        if max(counts) == 0:
            return ans * 2
        else:
            i = counts.index(max(counts))
            state1_row[i] = -1
            ans += 1
            return count_conflicts(state1_row, state2_row, n, ans)

    res = manhattan(state1, state2, n)
    state1_rows = [[] for y in range(n)] 
    state1_columns = [[] for x in range(n)] 
    state2_rows = [[] for y in range(n)] 
    state2_columns = [[] for x in range(n)] 
    for y in range(n):
        for x in range(n):
            idx = (y * n) + x
            state1_rows[y].append(state1[idx])
            state1_columns[x].append(state1[idx])
            state2_rows[y].append(state2[idx])
            state2_columns[x].append(state2[idx])
    for i in range(n):
            res += count_conflicts(state1_rows[i], state2_rows[i], n)
    for i in range(n):
            res += count_conflicts(state1_columns[i], state2_columns[i], n)
    return res

def misplaced_tiles(state1, state2, n):
    h = 0
    for i in range(n*n):
        if state1[i] != 0 and state1[i] != state2[i]:
            h += 1
    return h

def misplaced_positions(state1, state2, n):
    res = 0
    state1 = list(state1)
    state2 = list(state2)
    while state1 != state2:
        zi = state1.index(0)
        if state2[zi] != 0:
            sv = state2[zi]
            ci = state1.index(sv)
            state1[ci], state1[zi] = state1[zi], state1[ci]
        else:
            for i in range(n * n):
                if state2[i] != state1[i]:
                    state1[i], state1[zi] = state1[zi], state1[i]
                    break
        res += 1
    return res

def binary_search(array,thing):
    first = 0
    last = len(array)-1
    low = -1
    high = -1
    while first <= last:
        mid = (first + last)//2
        if array[mid]>thing:
            last = mid - 1
        elif array[mid]<thing:
            first = mid + 1
        else:
            return mid
    return first

def makeNode(current_node,goal_state,queue,heuristic,direct,q,SIZE,visited):
    if opposite(current_node)!=direct:
        temp_state, pos = swap(current_node.state,current_node.position,SIZE,direct)
        if temp_state != None:
            index = binary_search(visited,temp_state)
            if len(visited) == index or visited[index] != temp_state:
                temp_node = Node(temp_state,current_node.totalCost+1,pos)
                temp_node.parent = direct
                
                h = heuristic(temp_node.state, goal_state,SIZE)

                #Each Queue item is (F(n) , Order put in, node)
                #queue.put((temp_node.totalCost + h,10000000000-q,temp_node)) # This is LIFO
                queue.put((temp_node.totalCost + h,q,temp_node)) # This is FIFO        
                q+=1
    return q


class Node:
    state = None
    totalCost = None #Cost so far 
    parent = None
    position = None # position of the blank so swapping will be slightly faster
    hCost = None
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
print("Goal State : " , goal_state)

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

for i in range(100):
    #Create the random starting state
    while True:
        current_state,pos = createRandom(SIZE*SIZE)
        if possible(current_state,pos,SIZE) and current_state not in used:
            used.append(current_state):
            current_node = Node(current_state,0,pos)
            #current_node.hCost = FUNCTION(current_state, goal_state,SIZE)
            current_node.display(SIZE)
            break
        
    visited = []
    searching = PriorityQueue()
    num_node = 0    

    while not match(current_node.state,goal_state): # Should not be an infinite loop due to disorder check
        #Add each children to the priority Queue
        q=makeNode(current_node,goal_state,searching,FUNCTION,1,q,SIZE,visited) # UP
        q=makeNode(current_node,goal_state,searching,FUNCTION,2,q,SIZE,visited) # Right
        q=makeNode(current_node,goal_state,searching,FUNCTION,3,q,SIZE,visited) # Down
        q=makeNode(current_node,goal_state,searching,FUNCTION,4,q,SIZE,visited) # Left

        #Add current node as one that is already visited
        index = binary_search(visited,current_node.state)
        visited.insert(index,current_node.state)
        
        num_node += 1

        #Take the next node that has the smallest value
        current_node = searching.get()[2]
        
    print("FINISHED PUZZLE NUMBER {}".format(i+1))
    print("Path Cost: {}".format(current_node.totalCost))
    print("Number of Nodes Expanded: {}".format(num_node))
    
    solutionCost.append(current_node.totalCost)
    nodeCost.append(num_node)

print("Solution Cost : " , solutionCost)
print("Node Cost : " , nodeCost)
