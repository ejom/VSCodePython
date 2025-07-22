"""
Increment along each event.
Accumulate any events that fit.
Once you max out time/k or reach last event go back to prevous event you accumulated and mark that one you went back from to be skipped.

Keep track of max value and its corrisponding events
"""

"""
determine if an event fits
append start and end indexes to event
check each gap
"""

def maxValue(events: list[list[int]], k: int) -> int:
    maxEvent = [0, 0, 0]
    #Increment along each event
    refEvents = events.copy()
    for i, event in enumerate(refEvents):
        event[0] = (event[0],)
        event[1] = (event[1],)
        print(f"Round {i}: {event}")
        print()
        K = k-1
        #Increment along each later event
        nextEvents = events[i+1:]
        while True:
            lEvent = None
            pEvent = event
            for j, nEvent in enumerate(nextEvents):
                #If the day is filled or k is used up break
                if K==0:
                    print("Out of events")
                    print(event)
                    print()
                    break
                #if an event fits accumulate val
                hasOverlap = False
                for startTime, endTime in zip(event[0], event[1]):
                    #Check for any overlap For each time block
                    if nEvent[0] in range(startTime, endTime+1) or nEvent[1] in range(startTime, endTime+1):
                        hasOverlap = True
                if not hasOverlap:
                    print("storing previous values")
                    pEvent = event.copy()
                    print(pEvent)
                    event[0]+=(nEvent[0],)
                    event[1]+=(nEvent[1],)
                    event[2] += nEvent[2]
                    K-=1
                    lEvent = nEvent
                print(f"update {j}: {event}")
            #undo the last event that fit, mark it to be always skipped, 
            #and repeat
            if event[2]>maxEvent[2]:
                maxEvent = event
            #If you go back and dont accumulate anything you can continue
            if not lEvent:
                break
            nextEvents.remove(lEvent)
            event = pEvent
            K += 1
            print("Reverted Event")
            print(event)
            print()
    return maxEvent[2]
events=[[87,95,42],[3,42,37],[20,42,100],[53,84,80],[10,88,38],[25,80,57],[18,38,33]]
print(maxValue(events, 3))

"""
Find all event combinations
return greatest

For each event
"""