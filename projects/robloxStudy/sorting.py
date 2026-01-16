class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        #If the beginning and/or end of a an interval lies in another merge
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]
        for i in range(1, len(intervals)):
            start=intervals[i][0]
            end=intervals[i][1]
            last_start = merged[-1][0]
            last_end = merged[-1][1]

            if start<=last_end:
                if end<=last_end:
                    continue
                merged[-1][1] = end
            else:
                merged.append([start, end])

        return merged

            

        