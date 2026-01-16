def findTheCity(n: int, edges, distanceThreshold: int) -> int:
    INF = 10**15

    # dist[i][j] = shortest distance from i to j
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0

    # undirected edges
    for u, v, w in edges:
        # keep the smallest weight if duplicates ever appear
        if w < dist[u][v]:
            dist[u][v] = w
            dist[v][u] = w

    # Floyd–Warshall: O(n^3)
    for k in range(n):
        for i in range(n):
            # small pruning: if i->k already too big, skip inner j
            if dist[i][k] > distanceThreshold:
                continue
            dik = dist[i][k]
            for j in range(n):
                nd = dik + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd

    best_city = -1
    best_count = 10**9

    for i in range(n):
        count = sum(1 for j in range(n) if i != j and dist[i][j] <= distanceThreshold)
        # tie-break: choose greatest index on equal count
        if count <= best_count:
            best_count = count
            best_city = i

    return best_city

print(findTheCity(4, [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], 4))