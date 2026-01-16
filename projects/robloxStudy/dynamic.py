def coinChange(coins, amount: int) -> int:
    # Create a dp array to store the minimum coins for each amount.
    # Initialize with a value larger than any possible answer (amount + 1).
    dp = [amount + 1] * (amount + 1)
    
    # The number of coins to make amount 0 is 0. This is our base case.
    dp[0] = 0
    
    # Iterate from amount 1 up to the target amount.
    for i in range(1, amount + 1):
        # For each amount, check every coin.
        for coin in coins:
            # If the coin can be used to make up the current amount...
            if i - coin >= 0:
                # ...update the dp array with the minimum number of coins.
                # The choice is either the current value of dp[i] or
                # 1 (for the current coin) + the value for the remaining amount.
                dp[i] = min(dp[i], 1 + dp[i - coin])
                
    # After the loops, if dp[amount] is still our initial large value,
    # it means the amount cannot be made. Otherwise, we found the answer.
    if dp[amount] == amount + 1:
        return -1
    else:
        return dp[amount]
    
print(coinChange([1, 2, 5], 11))