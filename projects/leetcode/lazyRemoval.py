import heapq
from collections import defaultdict

class NumberContainers:
    def __init__(self):
        # Maps index -> current number at that index
        self.index_to_num = {}
        # Maps number -> Min-Heap of indices that HAVE (or HAD) this number
        self.num_to_indices = defaultdict(list)

    def change(self, index: int, number: int) -> None:
        # Update what is currently at this index
        self.index_to_num[index] = number
        # Add this index to the heap for this number
        heapq.heappush(self.num_to_indices[number], index)

    def find(self, number: int) -> int:
        if number not in self.num_to_indices:
            return -1
        
        heap = self.num_to_indices[number]
        
        # Lazy Removal: Check if the smallest index in the heap 
        # actually still points to this number in our master dictionary
        while heap:
            smallest_index = heap[0]
            if self.index_to_num.get(smallest_index) == number:
                return smallest_index
            else:
                # This index has been replaced by a different number, 
                # so this heap entry is "stale". Pop it.
                heapq.heappop(heap)
                
        return -1