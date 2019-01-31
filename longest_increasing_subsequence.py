#!/usr/bin/python3
import random
from time import perf_counter
import logging
numeric_level = getattr(logging, 'INFO', None)
logging.basicConfig(datefmt='#(%Z) %d:%m:%Y %I:%M:%S %p', format='%(asctime)s %(levelname)-8s  %(message)s', level=numeric_level)
"""Problem : Given a sequence of numbers, find the longest increasing sequence
             Example:  2 4 5 6 7 4 3 2 1 , the longest increasing subsequnce would be 2 4 5 6 7
             Brute force: Number of possible solutions = 2 ** n
             By Dynamic programming, let us guess an edge to be a part of the LIS, in a graph where edge u,v exists iff u < v
             Now, the problem would be to find a longest path in the graph formulated.
Input : An array of numbers
Output : A longest possible increasing subsequence"""
 
def func_logger(func):
    def inner(*args, **kwargs): 
        t0 = perf_counter()
        result = func(*args, **kwargs)
        t1 = perf_counter()
        logging.info("func: {} took {:.6f} with {} as args->{}".format(func.__name__, (t1-t0) , args,result))    
        return result
    return inner

class Node:    
    def __init__(self, x):
        self.data = x
        # A random 'unique' value to be used by the hashing algorithm. Helps to distinguish nodes having same data.
        self.x = random.random() * 10000
    
    def __eq__(self, other):
        return self.x == other.x

    def __lt__(self, other):
        return self.data < other.data 
    
    def __repr__(self):
        return str(self.data)
    
    def __hash__(self):
        return hash(self.x)

class Graph:
    """represents a graph, a tuple of vertics, edges between them"""
    v = []
    e = {}
    def __init__(self, v, e=None):
        # Create node objects for all data points.
        for i in v:           
            self.v.append(Node(i))     
              
        if e is None:
            self.create_edges()
        else:
            self.e = dict(e)

    def create_edges(self):
        """Create edges. edge (u,v) exists iff u < v"""
        for i in range(len(self.v)-1):
            pivot = self.v[i]
            for j in range(i, len(self.v)):
                elem = self.v[j]
                if i == j:
                    continue
                else:
                    if pivot < elem:
                        # plot an edge from i to j                        
                        self.e.setdefault(pivot, []).append(elem)
        
def reverse_Graph(G):
    """Reverse the Graph G"""
    u_e = {}
    for u,v in G.e.items():
        for x in v:
            u_e.setdefault(x, []).append(u)
    v  = list(G.v)
    return Graph(v, u_e)

@func_logger
def create_graph(n):
    """For a given array of n numbers, creates a graph of n nodes where every edge u,v obeys the property u < v """
    g = Graph(n)       
    return g

def print_node(k, size, inner_size):
    """Some nice way to represenet a Graph node."""
    print('*' * size)
    for i in range(inner_size):
        print('*' + ' ' * (inner_size//2) + str(k)+' ' * (inner_size//2) + '*')
    print('*' * size)

@func_logger    
def get_lIs(n):
    """L[i]: longest increasing sequence ending at i"""
    print("The auto-generated sequence: {}".format(n))
    L = {}
    predecessor = {}
    G = create_graph(n)    
    Gr = reverse_Graph(G)    
    for v in G.v:        
        temp = {x:L[x] if  isinstance(x, Node) else 0 for x in Gr.e.get(v, [-99])}        
        predecessor[v] = max(temp, key=lambda x : temp[x])
        L[v] = max(temp.values()) + 1    

    max_seq_length, k = (max((L[x],x) for x in L))
    print('length of longest increasing sequence: {}\n\n'.format(max_seq_length))
    print('The sequence is:')   
    size = 5
    offset = 0
    # If predecessor[k] is not a Node obj, it has to be -99.
    while(isinstance(predecessor[k], Node)):       
        inner_size = 5 - 2         
        print_node(k, size, inner_size)        
        print(u'\N{BLACK UP-POINTING TRIANGLE}')                   
        k = predecessor[k]
    print_node(k, size, inner_size)
    
for i in range(1):
    # random.choices picks 'k' objects with repetition.
    get_lIs([int(x) for x in random.choices(range(50), k=10)])
