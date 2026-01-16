import heapq
from collections import defaultdict

"""
You are given a network of n nodes, labeled from 1 to n. You are also given times, a list of travel 
times as directed edges times[i] = (ui, vi, wi), where ui is the source node, vi is the target node, 
and wi is the time it takes for a signal to travel from source to target.

We will send a signal from a given node k. Return the minimum time it takes for all the n nodes to 
receive the signal. If it is impossible for all the n nodes to receive the signal, return -1.
"""

def networkDelayTime(times, n, k):
    # 1. Build the adjacency list: source -> [(target, weight), ...]
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    
    # 2. Priority Queue: (time_to_reach_node, node)
    # Start with node k at time 0
    pq = [(0, k)]
    
    # Dictionary to store the shortest time to each node
    visited = {}
    
    while pq:
        time, curr_node = heapq.heappop(pq)
        
        # If we've already found a shorter path to this node, skip it
        if curr_node in visited:
            continue
        
        # Record the shortest time for this node
        visited[curr_node] = time
        
        # Explore neighbors
        for neighbor, weight in graph[curr_node]:
            if neighbor not in visited:
                heapq.heappush(pq, (time + weight, neighbor))
    
    # 3. Check results
    # If we haven't visited all n nodes, return -1
    if len(visited) < n:
        return -1
    
    # The total time is the maximum of the shortest times recorded
    return max(visited.values())

print(networkDelayTime([[1,2,1],[2,3,1],[3,4,1], [4, 5, 1], [1, 6, 2], [6, 5, 2]], 6, 1))