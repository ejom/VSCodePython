from collections import deque

class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        # 1. Build the graph and calculate indegrees
        adj = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        
        for course, prereq in prerequisites:
            adj[prereq].append(course)
            indegree[course] += 1
            
        # 2. Add all courses with no prerequisites to the queue
        queue = deque([i for i in range(numCourses) if indegree[i] == 0])
        
        # 3. Process the queue
        taken_courses = 0
        while queue:
            current = queue.popleft()
            taken_courses += 1
            
            # For every course that depends on the current one
            for neighbor in adj[current]:
                indegree[neighbor] -= 1
                # If all prerequisites are now met
                if indegree[neighbor] == 0:
                    queue.append(neighbor)
        
        # 4. If we took all courses, there was no cycle
        return taken_courses == numCourses