# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    # bfs
    # Implemented with Queue s.t. each element is of form
    #   (node,path_to_this_node)
    # Returns found path or (if unsuccessful) last path explored

    curr = curr_path = start
    Q = [(curr,curr_path)]
    visited = set()
    while len(Q) > 0 and curr != goal:
        curr, curr_path = Q.pop(0)
        visited.add(curr)
        Q += [ (n, curr_path + n) for n in graph.get_connected_nodes(curr) if n not in visited ]

    return curr_path

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal, predicate=None):

    current_node = start
    current_path = [start]
    stack = [(current_node, current_path)]
    extended = set()

    while len(stack) != 0 and current_node != goal:
        current_node, current_path = stack.pop()
        extended.add(current_node)
        expanded = [(n, current_path + [n]) for n in graph.get_connected_nodes(current_node) if n not in extended]
        if predicate:
            stack += reversed(sorted(expanded, key=predicate))
        else:
            stack += expanded

    return current_path


def dfs_recursive(graph, start, goal, predicate=None):
    # dfs
    # simple recursive implementation

    graph.mark_node(start)

    if start == goal:
        return goal

    adj_unexplored = [n for n in graph.get_connected_nodes(start) if not graph.is_marked(n)]

    if len(adj_unexplored) == 0:
        # failing base case
        return None

    for n in adj_unexplored:
        print n
        if predicate and predicate(n) > predicate(start):
            print "tossing out",n
            continue
        else:
            path = dfs(graph, n, goal)
            if path:
                return start + path


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    # hill_climbing
    # it's DFS, but sorting nodes by heuristic predicate
    # for some reason, the tester expects a list
    path = dfs(graph, start, goal, predicate=lambda x: graph.get_heuristic(x[0],goal))
    return [n for n in path] if path else None


## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    curr = curr_path = start
    Q = [(curr,curr_path)]
    visited = set()
    while len(Q) > 0 and curr != goal:
        curr, curr_path = Q.pop(0)
        visited.add(curr)
        Q += [ (n, curr_path + n) for n in graph.get_connected_nodes(curr) if n not in visited ]
        Q = sorted(Q, key=lambda x: graph.get_heuristic(x[0],goal))[:beam_width]

    return [n for n in curr_path] if curr_path else None

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    length = 0
    for i,node in enumerate(node_names):
        try:
            adj = node_names[i+1]
        except IndexError:
            # reached end of the list
            break
        connected_nodes = graph.get_connected_nodes(node)
        if adj in connected_nodes:
            length += graph.get_edge(node, adj).length
        else:
            # next node in path list is not in adj list
            break

    return length



def branch_and_bound(graph, start, goal):
    raise NotImplementedError

def a_star(graph, start, goal):
    raise NotImplementedError


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    raise NotImplementedError

def is_consistent(graph, goal):
    raise NotImplementedError

HOW_MANY_HOURS_THIS_PSET_TOOK = ''
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
