import pandas as pd
import matplotlib.pyplot as plt
from numpy import sin, exp
import numpy as np
from scipy.optimize import curve_fit

def analyze_stock_CSV(CSV_file_name: str):
    df = pd.read_csv(CSV_file_name)

    df["datetime"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
    t0 = df["datetime"].min()  # reference date (start)
    df['date_val'] = (df["datetime"] - t0).dt.total_seconds() / 86400.0  # days as float

    # Example
    # df["Volume"] = ["1.1M", "2.3B", "500K", "123456"]  # K/none will just be treated as raw numbers

    # 1) Extract the numeric part
    df["vol_num"] = (
        df["Volume"]
        .str.replace(",", "", regex=False)        # remove commas if any
        .str.extract(r"([\d\.]+)")[0]
        .astype(float)
    )

    # 2) Extract the suffix (M/B) if present
    suffix = df["Volume"].str.extract(r"([MB])", expand=False)

    # 3) Map suffix to multiplier
    factor = suffix.map({"M": 1e6, "B": 1e9}).fillna(1)

    # 4) Final numeric volume
    df["Volume"] = df["vol_num"] * factor

    # Optional: drop helper column
    df = df.drop(columns=["vol_num"])


    vol_min = df['Volume'].min()
    vol_max = df['Volume'].max()
    max_weight = 2
    min_weight = 1

    df['Vol_Norm'] = min_weight + (df['Volume'] - vol_min) * (max_weight-min_weight)/(vol_max-vol_min)

    df['Weighted_High'] = df['Vol_Norm'] * df['High']
    df['Weighted_Low'] = df['Vol_Norm'] * df['Low']

    def model(x, k, p1, p2, p3, a, w, th):
        return k + p1*x + p2*x**2 + p3*x**3 + a*sin(w*x+th)
    
    popt_high, _ = curve_fit(model, df['date_val'], df['Weighted_High'])
    popt_low, _ = curve_fit(model, df['date_val'], df['Weighted_Low'])

    print("weighted high coefficients and prediction")
    print(popt_high)
    print("weighted low coefficients and prediction")
    print(popt_low)

    #Find the normalization factor for average Volume
    avg_vol_norm = min_weight + (df['Volume'].mean() - vol_min) * (max_weight-min_weight)/(vol_max-vol_min)
    print(f"Avg vol norm factor: {avg_vol_norm}")

    print("predictions for 11/14/26")
    print("Predicted High")
    print(model(2143+365, *popt_high)/avg_vol_norm)
    print("Predicted Low")
    print(model(2143+365, *popt_low)/avg_vol_norm)
    
    plt.subplot(2, 2, 1)
    plt.plot(df['date_val'], df['High'], label='High')
    plt.plot(df['date_val'], df['Low'], label='Low')
    plt.legend()
    plt.subplot(2, 2, 2)
    plt.plot(df['date_val'], df['Vol_Norm'])
    plt.title('Volume Normalized')

    plt.subplot(2, 2, 3)
    plt.plot(df['date_val'], df['Weighted_High'])
    plt.title('Weighted_High')
    plt.subplot(2, 2, 4)
    plt.plot(df['date_val'], df['Weighted_Low'])
    plt.title('Weighted_Low')

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.plot(df['date_val'], df['Weighted_High'])
    plt.plot(df['date_val'], model(df['date_val'], *popt_high))
    plt.title('Weighted High Regression Model')
    plt.subplot(1, 2, 2)
    plt.plot(df['date_val'], df['Weighted_Low'])
    plt.plot(df['date_val'], model(df['date_val'], *popt_low))
    plt.title('Weighted Low Regression Model')

    plt.show()
    
print("Google analysis:")
analyze_stock_CSV('Alphabet_A_Stock_Price_History.csv')
print()
print("NVIDIA analysis:")
analyze_stock_CSV('NVIDIA_Stock_Price_History.csv')