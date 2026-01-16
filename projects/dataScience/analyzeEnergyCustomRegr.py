import numpy as np
from sklearn.metrics import r2_score
import pandas as pd
from numpy import exp, sin, cos, log
from scipy.optimize import curve_fit

df_con = pd.read_csv('primary-consumption-by-major-source.csv')
df_prod = pd.read_csv('primary-energy-production-by-major-source-history.csv')

def analyze_df(df, isProd=False):
    electric_total = 0.138702180298
    electric_nuclear = 0.329417678207
    electric_fossil = 0.0992639699961
    
    if isProd:
        df.columns = ['Year', 'coal', 'natural gas', 'crude oil', 'NGPL', 'nuclear', 'renewables']
    else:
        df.columns = ['Year', 'coal', 'natural gas', 'petroleum', 'nuclear', 'renewables']
    df = df.iloc[5:].copy()

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    if isProd:
        energy_columns = ['coal', 'natural gas', 'crude oil', 'NGPL', 'nuclear', 'renewables']
        fossil_fuels = ['coal', 'natural gas', 'crude oil', 'NGPL']
    else:
        energy_columns = ['coal', 'natural gas', 'petroleum', 'nuclear', 'renewables']
        fossil_fuels = ['coal', 'natural gas', 'petroleum']

    #print(df)
    print("Total")
    df['Total'] = df[energy_columns].sum(axis=1)
    print(df['Total'].iloc[-3:])
    
    print('Fossil Fuels')
    df['fossil_totals'] = df[fossil_fuels].sum(axis=1)
    print(df['fossil_totals'].iloc[-3:])

    print('Nuclear')
    print(df['nuclear'].iloc[-3:])

    #Build regression model
    def pred_vals(category, electric_factor):
        split = 2000

        trainSet = df[df['Year']<split][category]
        testSet = df[df['Year']>=split][category]
        
        bestModel = None
        bestR2 = float('-inf')
        for deg in range(0, 7):
            model = np.poly1d(np.polyfit(df[df['Year']<split]['Year'], trainSet, deg=deg))
            r2 = r2_score(testSet, [model(y) for y in df[df['Year']>=split]['Year']])
            #print(r2)
            if r2>bestR2:
                bestDeg = deg
                bestR2 = r2
                bestModel = model
        
        print()
        print(f"predicted for {category}")
        if not bestModel:
            print("no fit")
            return
        print(f"Degree: {bestDeg}")
        print(f"R2 score of test set: {bestR2}")
        print(f"2026: {bestModel(2026)}")
        print(f"2027: {bestModel(2027)}")

        if isProd:
            print("predicted electrical generation")
            print(f"2026: {bestModel(2026)*electric_factor}")
            print(f"2027: {bestModel(2027)*electric_factor}")
    
    pred_vals('Total', electric_total)
    pred_vals('fossil_totals', electric_fossil)
    pred_vals('nuclear', electric_nuclear)

print("Analyzing consumption")
print()
analyze_df(df_con)

print()
print("Analyzing production")
analyze_df(df_prod, True)