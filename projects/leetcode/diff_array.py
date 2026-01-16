"""
There are n flights that are labeled from 1 to n.

You are given an array of flight bookings bookings, where bookings[i] = [firsti, lasti, seatsi] represents a booking for flights firsti through lasti (inclusive) with seatsi seats reserved for each flight in the range.

Return an array answer of length n, where answer[i] is the total number of seats reserved for flight i.
"""

class Solution:
    def corpFlightBookings(self, bookings: list[list[int]], n: int) -> list[int]:
        # Initialize the difference array with 0s
        # We use size n so we can map flight labels (1-indexed) to 0-indexed easily
        diff = [0] * n
        
        for first, last, seats in bookings:
            # Mark the start of the booking (1-indexed to 0-indexed)
            diff[first - 1] += seats
            
            # Mark the end of the booking
            # We subtract the seats at index 'last' because the seats 
            # are inclusive up to 'last', so the drop-off happens at 'last + 1'
            if last < n:
                diff[last] -= seats
        
        # Calculate the prefix sum to transform the difference array into the answer
        for i in range(1, n):
            diff[i] += diff[i - 1]
            
        return diff
    