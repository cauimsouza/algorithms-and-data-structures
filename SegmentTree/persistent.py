from collections import defaultdict
from bisect import bisect_right
from math import inf

_INF = 10_000_000_000

class Node:
    __slots__ = ['value', 'left', 'right']

    def __init__(self, value=_INF, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class SegmentTree:
    def __init__(self, n, root=None):
        self.n = n
        self.root = root if root else Node()

    def update(self, index: int, value: int) -> "SegmentTree":
        def f(node, l, r):
            if l == r:
                return Node(value)
            
            new_node = Node()

            mid = (l + r) // 2
            if index <= mid:
                new_node.left = f(node.left if node and node.left else None, l, mid)
                new_node.right = node.right if node else None
            else:
                new_node.left = node.left if node else None
                new_node.right = f(node.right if node and node.right else None, mid + 1, r)

            left_value = new_node.left.value if new_node.left else _INF
            right_value = new_node.right.value if new_node.right else _INF
            new_node.value = min(left_value, right_value)

            return new_node
        return SegmentTree(self.n, f(self.root, 0, self.n - 1))
    
    def get_min(self, left: int, right: int) -> int:
        def f(node, l, r):
            if not node or right < l or r < left:
                return _INF
            if left <= l and r <= right:
                return node.value
            
            mid = (l + r) // 2
            return min(f(node.left, l, mid), f(node.right, mid + 1, r))

        return f(self.root, 0, self.n - 1)
