def uniquePathsWithObstacles(obstacleGrid):
    if not obstacleGrid or obstacleGrid[0][0] == 1:
        return 0
    
    m, n = len(obstacleGrid), len(obstacleGrid[0])
    # Use a 1D DP array to save space
    dp = [0] * n
    dp[0] = 1
    
    for i in range(m):
        for j in range(n):
            if obstacleGrid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                # The current dp[j] is the value from the top (i-1, j)
                # dp[j-1] is the value from the left (i, j-1)
                dp[j] += dp[j-1]
                
    return dp[-1]

grid = [
    [0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 1, 0],
    [1, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0]
]

gridEmpty = [[0]*3]*3

print(uniquePathsWithObstacles(gridEmpty))