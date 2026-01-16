class SolutionRec:
    def closestCostRec(self, baseCosts: list[int], toppingCosts: list[int], target: int) -> int:
        self.closest = baseCosts[0]
        
        def dfs(current_cost, topping_idx):
            # Update the global closest if this current_cost is better
            diff = abs(current_cost - target)
            best_diff = abs(self.closest - target)
            
            if diff < best_diff:
                self.closest = current_cost
            elif diff == best_diff:
                self.closest = min(self.closest, current_cost)
            
            # Optimization: If current_cost is already much larger than target, 
            # adding more toppings won't help us find a closer (smaller) value.
            if current_cost >= target or topping_idx == len(toppingCosts):
                return
            
            # Each topping can be added 0, 1, or 2 times
            for count in range(3):
                dfs(current_cost + count * toppingCosts[topping_idx], topping_idx + 1)

        # Try every base as a starting point
        for base in baseCosts:
            dfs(base, 0)
            
        return self.closest