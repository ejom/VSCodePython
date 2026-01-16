import pandas as pd

# 1. Setup sample data
data = {'Values': [10, 20, 30, 40]}
df = pd.DataFrame(data)

# 2. Calculate cumulative statistics
df['Cum_Avg'] = df['Values'].expanding().mean()
df['Cum_Std'] = df['Values'].expanding().std()

print(df)