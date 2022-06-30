import collections
from data import *

# dfs
def dfs(start,end):
    global tilesRepresentation
    stack = collections.deque([[start]])
    seen = set([start])
    while stack:
        path = stack.pop()
        x, y = path[-1]
        if x == end[0] and y == end[1]:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < len(tilesRepresentation) :
                if 0 <= y2 < len(tilesRepresentation[0]) :
                    if tilesRepresentation[x2][y2] != 'W' :
                        if (x2, y2) not in seen:
                            stack.append(path + [(x2, y2)])
                            seen.add((x2, y2))
    return []


# A STAR
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position

def return_path(current_node,maze):
    path = []

    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent

    return path[::-1]


def aStar(maze, start, end):

    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    yet_to_visit_list = []  

    visited_list = [] 
    
    yet_to_visit_list.append(start_node)
    

    move  =  [[-1, 0 ], # go up
              [ 0, -1], # go left
              [ 1, 0 ], # go down
              [ 0, 1 ]] # go right

    no_rows, no_columns = len(maze) , len(maze[0])
    
    while len(yet_to_visit_list) > 0:
  
        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
                
        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        if current_node == end_node:
            return return_path(current_node,maze)

        children = []
        for new_position in move: 
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if (node_position[0] > (no_rows - 1) or 
                node_position[0] < 0 or 
                node_position[1] > (no_columns -1) or 
                node_position[1] < 0):
                continue

            if maze[node_position[0]][node_position[1]] == 'W':
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:

            flag = False
            for node in yet_to_visit_list:
                if child.g > node.g:
                    flag = True
                    break

            if child in visited_list or (flag and child in yet_to_visit_list):
                continue

            child.g = current_node.g + 1
            child.h = (((child.position[0] - end_node.position[0]) ** 2) + 
                       ((child.position[1] - end_node.position[1]) ** 2)) 

            child.f = child.g + child.h
            if child not in visited_list:
                yet_to_visit_list.append(child)
    return []


# bfs
def bfs(start,end):
    global tilesRepresentation
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if x == end[0] and y == end[1]:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < len(tilesRepresentation) :
                if 0 <= y2 < len(tilesRepresentation[0]) :
                    if tilesRepresentation[x2][y2] != 'W' :
                        if (x2, y2) not in seen:
                            queue.append(path + [(x2, y2)])
                            seen.add((x2, y2))
    return []
