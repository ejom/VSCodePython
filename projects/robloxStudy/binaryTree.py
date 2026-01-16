# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # Initial call to the helper function with infinite bounds
        return self.checkTree(root, float('-inf'), float('inf'))

    def checkTree(self, root: Optional[TreeNode], min_val: float, max_val: float) -> bool:
        # Base case: an empty node is a valid BST
        if not root:
            return True
        
        # A node's value must be within the specified range (min_val, max_val)
        if not (min_val < root.val < max_val):
            return False
            
        # Recursively check the left and right subtrees
        # For the left subtree, the upper bound is the current node's value.
        # For the right subtree, the lower bound is the current node's value.
        return self.checkTree(root.left, min_val, root.val) and self.checkTree(root.right, root.val, max_val)