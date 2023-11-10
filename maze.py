"""First in first out 

Current Node
Frontier

Is the current Node the end goal?
Add the current node to the explored list
Add the two nodes connected to the Frontier
Pick a node and and repeat; 

Frontier Array - with max 10 items
Node
Explored array

For x = 1 to 10
If Node = array(x)
    Found the node  
else
    x+!, Explore array =array(x)
""" 

  
import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []
    def add(self, node):
        self.frontier.append(node)
    def contains_state(self,state):
        return any(node.state == state for node in self.frontier)
    def empty(self):
        return len(self.frontier) ==0
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
          node = self.frontier[-1]
          self.frontier = self.frontier[:-1]
          return node
class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():










      
