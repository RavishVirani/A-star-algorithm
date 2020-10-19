from collections import deque
import random
from queue import PriorityQueue
import copy

num_nodes = int

def match(state1,state2):
    if len(state1) == len(state2):
        for i in range(len(state1)):
            if state1[i]!=state2[i]:
                return False
        return True
    return False

def swap(state,pos,n,direct):
    # 1==UP
    # 2==DOWN
    # 3==LEFT
    # 4==RIGHT
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
    # Returns the opposite direction of the swap function
    if direct ==1:
        return 2
    elif direct==2:
        return 1
    elif direct ==3:
        return 4
    elif direct ==4:
        return 3
    return 0

def disorder(state):
    total = 0
    for i in range(len(state)):
        for n in range(i+1,len(state)):
            if state[i]>state[n] and state[i]!=0 and state[n]!=0:
                total+=1
    return total

def possible(state,position,width):
    #Assume that the second state is the goal state [1,..,n,0]
    if width%2 ==1: #Odd Side Length
        return disorder(state)%2 == 0
    else: #Even Side Length
        y = position//width
        inversion = disorder(state)%2
        if y%2==0 and inversion==1:
            return True
        elif y%2==1 and inversion==0:
            return True
        return False

def iterative_main(root):
    bound = heuristic(root.state,goal_state,SIZE)
    stack = deque()
    while True:
        #print("The current Bound is: {}".format(bound))
        stack = deque()
        stack.append(root)
        value = iterative_helper(stack,bound)
        if value < 0:
            return -value
        bound = value
    return


def iterative_helper(stack,bound):
    global num_nodes
    node = stack[-1]
    num_nodes+=1
    if match(node.state,goal_state):
        return -node.totalCost
    total = node.totalCost + heuristic(node.state,goal_state,SIZE)
    
    if total>bound:
        return total
    smallest = float("inf")
    for i in range(1,5):
        if opposite(node.parent) != i:
            temp_state,pos = swap(node.state,node.position,SIZE,i)
            if pos is not None and temp_state not in stack:
                temp_node = Node(temp_state,node.totalCost+1,pos)
                temp_node.parent = i
                stack.append(temp_node)

                cost = iterative_helper(stack,bound)
                if cost < 0:
                    return cost
                if cost<smallest:
                    smallest = cost
                stack.pop()
    return smallest

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

class Node:
    state = None
    totalCost = None
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

SIZE = 4 # the side length of the puzzle. n where n creates an nxn puzzle

#The goal is [1,...,n^2-1,0]
# Ex for the 3x3 puzzle(8-puzzle): [1,2,3,4,5,6,7,8,0]
goal_state = list(range(1,SIZE*SIZE))
goal_state.append(0)

current_node = None
num_nodes = 0
path = 0
solutionCost = []
nodeCost = []
used = []

heuristic = misplaced_tiles
#heuristic = misplaced_positions
#heuristic = manhattan
#heuristic = linear_conflicts

for i in range(100):
    #Create the random starting state
    while True:
        current_state,pos = createRandom(SIZE*SIZE)
        if possible(current_state,pos,SIZE) and current_state not in used:
            used.append(current_state)
            current_node = Node(current_state,0,pos)
            current_node.display(SIZE)
            break
    num_nodes = 0
    path = iterative_main(current_node)
    
    solutionCost.append(path)
    nodeCost.append(num_nodes)
    print("Solved Puzzle {}".format(i+1))
    print("Path cost: {}".format(path))
    print("Nodes Expanded: {}".format(num_nodes))
    print()

print("All Solution Costs : " , solutionCost)
print("All Node Costs : " , nodeCost)
