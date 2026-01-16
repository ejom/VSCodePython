"""
Given the root of a Binary Search Tree (BST), convert it to a Greater Tree such that every 
key of the original BST is changed to the original key plus the sum of all keys greater than 
the original key in BST.
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def convertBST(self, root):
        running_sum = 0
        stack = []
        node = root

        while stack or node:
            # go as far right as possible
            while node:
                stack.append(node)
                node = node.right

            node = stack.pop()
            running_sum += node.val
            node.val = running_sum

            node = node.left

        return root
