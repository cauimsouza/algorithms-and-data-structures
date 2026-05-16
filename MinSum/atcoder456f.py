# Solution to problem https://atcoder.jp/contests/abc456/tasks/abc456_f, which requires basic knowledge of min-sum algebra

import math

def _multiply(M, N):
    res = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            res[i][j] = min(M[i][t] + N[t][j] for t in range(2))
    return res

class SegmentTree:
    def __init__(self, A: list[int]):
        self._n = n = len(A)
        self._M = [None] * (4 * n)

        self._build(1, 0, n - 1, A)
    
    def _build(self, node: int, left: int, right: int, A: list[int]) -> None:
        if left == right:
            self._M[node] = [[A[left], A[left]], [0, math.inf]]
            return
        
        mid = (left + right) // 2
        l, r = node * 2, node * 2 + 1
        self._build(l, left, mid, A)
        self._build(r, mid + 1, right, A)
        left_M, right_M = self._M[l], self._M[r]

        self._M[node] = _multiply(right_M, left_M)

    def get(self, left: int, right: int) -> int:
        def f(node: int, l: int, r: int) -> list[list[int]]:
            if r < left or l > right:
                return [[0, math.inf], [math.inf, 0]] # The neutral element of the min-sum algebra
            if left <= l and r <= right:
                return self._M[node]
            
            mid = (l + r) // 2
            Left, Right = f(node * 2, l, mid), f(node * 2 + 1, mid + 1, r)
            return _multiply(Right, Left)
        
        return f(1, 0, self._n - 1)[0][0]

def solve(A: list[int], k: int) -> int:
    n = len(A)

    st = SegmentTree(A)

    best = math.inf
    for left in range(n - k + 1):
        a = A[left] + st.get(left + 1, left + k - 1) # Sequence of length k
        b = A[left] + st.get(left + 1, left + k) if left + k < n else math.inf # Sequence of length k + 1
        best = min(best, a, b)
    return best

if __name__ == '__main__':
    T = int(input())
    for _ in range(T):
        _, k = map(int, input().split())
        A = list(map(int, input().split()))
        print(solve(A, k))