class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isSymmetric(root):
    if root is None:
        return True
    
    queue = [(root.left, root.right)]
    
    while queue:
        left_node, right_node = queue.pop(0)
        
        if left_node is None and right_node is None:
            continue
        if left_node is None or right_node is None:
            return False
        if left_node.val != right_node.val:
            return False
        
        
        queue.append((left_node.left, right_node.right))
        queue.append((left_node.right, right_node.left))
    
    return True


root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(2)
root.left.left = TreeNode(3)
root.left.right = TreeNode(4)
root.right.left = TreeNode(4)
root.right.right = TreeNode(3)

print(isSymmetric(root))  
