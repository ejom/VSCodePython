from collections import deque

class Solution:
    def findMinHeightTrees(self, n: int, edges: list[list[int]]) -> list[int]:
        # Edge case: If there are 1 or 2 nodes, they are the answer
        if n <= 2:
            return [i for i in range(n)]
        
        # Build adjacency list and track degrees
        adj = [set() for _ in range(n)]
        for u, v in edges:
            adj[u].add(v)
            adj[v].add(u)
            
        # Initialize the first layer of leaves
        leaves = deque()
        for i in range(n):
            if len(adj[i]) == 1:
                leaves.append(i)
        
        # Trim the onion until 2 or fewer nodes remain
        remaining_nodes = n
        while remaining_nodes > 2:
            leaves_count = len(leaves)
            remaining_nodes -= leaves_count
            
            # Remove the current layer of leaves
            for _ in range(leaves_count):
                leaf = leaves.popleft()
                # There is only one neighbor for a leaf
                neighbor = adj[leaf].pop()
                # Remove the connection from the neighbor's side
                adj[neighbor].remove(leaf)
                
                # If the neighbor becomes a leaf, add it to the queue
                if len(adj[neighbor]) == 1:
                    leaves.append(neighbor)
                    
        return list(leaves)
    
sol=Solution()
print(sol.findMinHeightTrees(6, [[3,0],[3,1],[3,2],[3,4],[5,4]]))