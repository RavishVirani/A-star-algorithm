from collections import deque
from general import disorder,match,createRandom,manhattan,swap,opposite,Node


def iterative_main(root):
    bound = heuristic(root.state)
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
    total = node.totalCost + heuristic(node.state,goal_state)
    
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

SIZE = 4 # the side length of the puzzle. n where n creates an nxn puzzle

goal_state = list(range(1,SIZE*SIZE))
goal_state.append(0)

current_node = None
num_nodes = 0
solutionCost = []
nodeCost = []
used = []

heuristic = manhattan

#TIME ISSUE Look for inefficiencies or translate to faster language?
for i in range(100):
    #Create the random starting state
    while True:
        current_state,pos = createRandom(SIZE*SIZE)
        if disorder(current_state)%2 == disorder(goal_state)%2 and current_state not in used: # the disorder of goal is even
            used.append(current_state)

            #current_state = [1,2,3,4,5,6,0,7,8]
            #pos = 6
            current_node = Node(current_state,0,pos)
            #current_node.hCost = heuristic(current_state, goal_state,SIZE)
            current_node.display(SIZE)
            break
    num_nodes = 0
    solutionCost.append(iterative_main(current_node))
    nodeCost.append(num_nodes)
    print("Solved Puzzle {}".format(i))

print(solutionCost)
print(nodeCost)
