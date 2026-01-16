import numpy as np
from sklearn.metrics import r2_score
import pandas as pd

df_vol = pd.read_csv('decile_oddlot_volume_stock.csv')
df_rate = pd.read_csv('decile_oddlot_rate_stock.csv')

def analyzeDF(df):
    new_df = df[df['Date']>=20200000]

    df_year = new_df.groupby(pd.cut(df['Date'], [0, 2021e4, 2022e4, 2023e4, 2024e4, 2025e4, 2026e4], labels=[2020, 2021, 2022, 2023, 2024, 2025]), observed=True).mean()
    df_price_year = df_year.filter(regex='Price')

    models = dict()
    end3qtrs_2025 = dict()
    r2_vals = dict()
    for col in df_price_year.columns:
        models[col] = np.poly1d(np.polyfit(df_price_year.index[:-1], df_price_year[col][:-1], deg=3))
        end3qtrs_2025[col] = (models[col](2025)*4-df_price_year[col].iloc[-1])/3
        r2_vals[col] = r2_score(df_price_year[col][:-1], [models[col](y) for y in range(2020, 2025)])

    return df_price_year, models, end3qtrs_2025, r2_vals

df_price_year_vol, models_vol, end3qtrs_2025_vol, r2_vals_vol = analyzeDF(df_vol)
df_price_year_rate, models_rate, end3qtrs_2025_rate, r2_vals_rate = analyzeDF(df_rate)

for col in df_price_year_vol.columns:
    print(col, end=", ")

print()
print("total average diff: ")
for row in range(6):
    print()
    print(2020+row)
    for col in df_price_year_vol.columns:
        if row<2025:
            print(df_price_year_rate[col].iloc[row]-df_price_year_vol[col].iloc[row], end=", ")
        else: 
            print(models_rate[col](2025) - models_vol[col](2025))

print()
print("R2 scores for rate")
for col in df_price_year_vol.columns:
    print(r2_vals_rate[col], end=", ")

print()
print("R2 scores for vol")
for col in df_price_year_vol.columns:
    print(r2_vals_vol[col], end=", ")

print()
print("Q1 average diffs 2025: ")
for col in df_price_year_vol.columns:
    print(df_price_year_rate[col].iloc[-1] - df_price_year_vol[col].iloc[-1], end=", ")

print()
print("Last 3Q average diff: ")
for col in df_price_year_vol.columns:
    print(end3qtrs_2025_rate[col] - end3qtrs_2025_vol[col], end=", ")






