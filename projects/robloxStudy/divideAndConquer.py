# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def __str__(self):
        while self:
            print(self.val)
            self = self.next
        return "done"

def sortList(head):
    if not head or not head.next:
        return head

    # Step 1: Divide the list into two halves
    slow, fast = head, head
    prev = None
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next
    
    # Split the list into two parts
    if prev:
        prev.next = None
    
    # Step 2: Recursively sort the two halves
    list1 = sortList(head)
    list2 = sortList(slow)

    # Step 3: Merge the two sorted halves
    return merge(list1, list2)

def merge(l1, l2):
    dummy = ListNode()
    current = dummy

    while l1 and l2:
        if l1.val < l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    # Attach any remaining nodes
    if l1:
        current.next = l1
    if l2:
        current.next = l2

    return dummy.next

print(sortList(ListNode(4, ListNode(2, ListNode(1, ListNode(3))))))