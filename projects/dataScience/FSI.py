import pandas as pd

Economic_score = {
    'Year': [i for i in range(2006, 2025)],
    'E1': [1.5, 1.8, 2.3, 2.9, 4.0, 3.7, 3.4, 3.2, 3.1, 2.8, 2.5, 2.4, 2.3, 2.1, 1.8, 2.1, 1.8, 2.1, 2.0],
    'Debt_to_GDP': [62, 63, 68, 82, 91, 96, 100, 100, 102, 100, 105, 104, 105, 107, 126, 123, 121, 121, 123]
}

df_eco = pd.DataFrame(Economic_score)
df_CPI_raw_full = pd.read_csv('CPI.csv')
df_CPI_raw = df_CPI_raw_full.iloc[:241].copy()
df_CPI_raw['All items'] = df_CPI_raw['All items'].str.replace('%', '').astype(float)
df_unemployment_raw = pd.read_csv('Unemployment.csv')

def group_year(df: pd.DataFrame, val: str):
    df = df.copy()
    df['Month'] = df['Month'].str.replace('Sept', 'Sep')
    df['Month'] = df['Month'].str.replace('June', 'Jun')
    df['Month'] = df['Month'].str.replace('July', 'Jul')
    df['Year'] = pd.to_datetime(df['Month'], format='%b %Y')
    return df.groupby(df['Year'].dt.year)[val].mean().reset_index()

df_CPI = group_year(df_CPI_raw, 'All items')
df_unemployment = group_year(df_unemployment_raw, 'Total')

df_mid = pd.merge(df_eco, df_CPI, on='Year')
df = pd.merge(df_mid, df_unemployment, on='Year')

df_norm = df.copy()
for col in df.columns[1:]:
    min = df[col].min()
    max = df[col].max()
    df_norm[col] = (df[col]-min)/(max-min)

df_norm['Avg'] = df_norm[['E1', 'Debt_to_GDP', 'All items', 'Total']].mean(axis=1)
min = df_norm['Avg'].min()
max = df_norm['Avg'].max()
df_norm['Avg'] = (df_norm['Avg'] - min)/(max-min)

print(df_norm)

from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# 1. Define your inputs (X) and target (y)
# We use the normalized data to ensure the weights aren't biased by scale
X = df_norm[['Debt_to_GDP', 'All items', 'Total']]
y = df_norm['E1']

# 2. Fit the model
model = LinearRegression()
model.fit(X, y)

# 3. Extract the optimal weights
weights = dict(zip(X.columns, model.coef_))
intercept = model.intercept_

print("--- Optimal Weights Found ---")
for col, w in weights.items():
    print(f"{col}: {w:.4f}")
print(f"Intercept: {intercept:.4f}")

# 4. Calculate the new 'Fitted' column using these weights
df_norm['Calculated_Fit'] = (
    (df_norm['Debt_to_GDP'] * weights['Debt_to_GDP']) +
    (df_norm['All items'] * weights['All items']) +
    (df_norm['Total'] * weights['Total']) +
    intercept
)

# Optional: Re-normalize the result to 0-1 if you want to keep strict scaling
fit_min = df_norm['Calculated_Fit'].min()
fit_max = df_norm['Calculated_Fit'].max()
df_norm['Calculated_Fit_Norm'] = (df_norm['Calculated_Fit'] - fit_min) / (fit_max - fit_min)

# 5. Visualize the comparison
plt.figure(figsize=(10, 6))
plt.plot(df_norm['Year'], df_norm['E1'], label='Target (E1)', linewidth=3, color='black')
plt.plot(df_norm['Year'], df_norm['Calculated_Fit'], label='Weighted Fit', linestyle='--', linewidth=2, color='red')
plt.plot(df_norm['Year'], df_norm['Avg'], label='Original Unweighted Avg', linestyle=':', alpha=0.5)
plt.legend()
plt.title('Optimization: Matching E1 Curve')
plt.grid(True, alpha=0.3)
plt.show()

# Print comparison
df_norm['diff'] = abs(df_norm['E1'] - df_norm['Calculated_Fit_Norm'])
print("\n--- Comparison ---")
print(df_norm[['Year', 'E1', 'Calculated_Fit_Norm', 'diff']])



