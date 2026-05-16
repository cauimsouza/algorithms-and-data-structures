# Solution to CSES problem Graph Paths II: https://cses.fi/problemset/task/1724/

import math

def multiply(A, B):
    n = len(A)
    return [[min(A[i][k] + B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def power(M, k):
    if k == 1:
        return M
    
    N = power(M, k // 2)
    if k % 2 == 0:
        return multiply(N, N)
    return multiply(multiply(N, N), M)

def solve(n: int, edges: list[list[int]], k: int) -> int:
    adj = [[math.inf] * n for _ in range(n)]
    for a, b, w in edges:
        adj[a - 1][b - 1] = min(adj[a - 1][b - 1], w)

    dist = power(adj, k)[0][n - 1]
    return dist if dist != math.inf else -1

if __name__ == '__main__':
    n, m, k = map(int, input().split())
    edges = [list(map(int, input().split())) for _ in range(m)]
    print(solve(n, edges, k))