from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def subtreeWithAllDeepest(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def dfs(node: Optional[TreeNode]):
            # returns (max_depth_from_node_down, subtree_root_answer)
            if not node:
                return -1, None  # depth -1 so leaf children become 0

            ld, lans = dfs(node.left)
            rd, rans = dfs(node.right)

            if ld == rd:
                return ld + 1, node
            elif ld > rd:
                return ld + 1, lans
            else:
                return rd + 1, rans

        return dfs(root)[1]
