import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

cons_raw_df = pd.read_csv('DAYTON_hourly.csv')
priceRate_raw_df = pd.read_csv('APU000072610.csv')
revenue_raw_df = pd.read_csv('revenue.txt', sep=' ', header=None, names=['date', 'Revenue (M Dollars)'])

#clean the dataframes
def clean_data_dates(df: pd.DataFrame, datetime_col, minYear=2019, maxYear=2024, format=None):
    #split datatime into individual columns
    df[datetime_col] = pd.to_datetime(df[datetime_col])

    df['Year'] = df[datetime_col].dt.year
    if format=='hour':
        df['Month'] = df[datetime_col].dt.month
        df['Day'] = df[datetime_col].dt.day
        df['Hour'] = df[datetime_col].dt.hour
    elif format=='month':
        df['Month'] = df[datetime_col].dt.month
    elif format=='quarter':
        df['Quarter'] = df[datetime_col].dt.quarter

    df.drop(datetime_col, axis=1, inplace=True)

    #Filter years into specified range
    df = df[(df['Year']>=minYear) & (df['Year']<=maxYear)]

    return df

#use custom range of years and then adjust the 7 year discrepency
cons_df = clean_data_dates(cons_raw_df, 'Datetime', 2012, 2017, format='hour')
cons_df['Year'] = cons_df['Year']+7

priceRate_df = clean_data_dates(priceRate_raw_df, 'observation_date', format='month')

revenue_df = clean_data_dates(revenue_raw_df, 'date', format='quarter')
revenue_df['Revenue (M Dollars)'] = revenue_df['Revenue (M Dollars)'].str.replace('$', '').str.replace(',', '').astype(int)

#clean data of duplicates and identify gaps
def clean_duplicates(df, format):
    if format=='hour':
        df.drop_duplicates(['Year', 'Month', 'Day', 'Hour'], keep='last', inplace=True)
    elif format=='month':
        df.drop_duplicates(['Year', 'Month'], keep='last', inplace=True)
    elif format=='quarter':
        df.drop_duplicates(['Year', 'Quarter'], keep='last', inplace=True)

def find_missing_dates(df, format):
    if format=='hour':
        df['datetime'] = (df['Year'].astype(str) + 
            df['Month'].astype(str).str.zfill(2) + 
            df['Day'].astype(str).str.zfill(2) + 
            df['Hour'].astype(str).str.zfill(2))
        df['datetime']=df['datetime'].astype(int)
        df.sort_values(by='datetime', inplace=True)

        df['diff'] = df['datetime'].diff()
        return df[(df['diff']!=1) & (df['Day']!=1) & (df['diff']!=77)]
    
    elif format=='month':
        df['datetime'] = (df['Year'].astype(str) + 
            df['Month'].astype(str).str.zfill(2))
        df['datetime']=df['datetime'].astype(int)
        df.sort_values(by='datetime', inplace=True)

        df['diff'] = df['datetime'].diff()
        return df[(df['diff']!=1) & (df['Month']!=1)]
    
    elif format=='quarter':
        df['datetime'] = (df['Year'].astype(str) + 
            df['Quarter'].astype(str))
        df['datetime']=df['datetime'].astype(int)
        df.sort_values(by='datetime', inplace=True)

        df['diff'] = df['datetime'].diff()
        return df[(df['diff']!=1) & (df['Quarter']!=1)]
    
clean_duplicates(cons_df, format='hour')
clean_duplicates(priceRate_df, format='month')
clean_duplicates(revenue_df, format='quarter')

find_missing_dates(cons_df, format='hour')
find_missing_dates(priceRate_df, format='month')
find_missing_dates(revenue_df, format='quarter')
"""
cons_df.reset_index()
priceRate_df.reset_index()
revenue_df.reset_index()
"""

#Building the extra plots

monthly_power_df = cons_df.groupby(['Year', 'Month'])['Consumption MW'].sum().reset_index()
monthly_power_df['Rate'] = priceRate_df['dollars per kW'].values
monthly_power_df['Cost'] = monthly_power_df['Consumption MW']*monthly_power_df['Rate']*1e3

annual_power_df = cons_df.groupby('Year')['Consumption MW'].sum().reset_index()
annual_power_df['Cost'] = monthly_power_df.groupby('Year')['Cost'].sum().values

print()
print("Recent year percent revenue")
print(annual_power_df['Cost'].iloc[-1] / (revenue_df['Revenue (M Dollars)'].iloc[-4:].sum()*1e6))

monthly_power_df['Quarter'] = (monthly_power_df['Month'] - 1) // 3 + 1
quarterly_power_df = monthly_power_df.groupby(['Year', 'Quarter'])['Cost'].sum().reset_index()
quarterly_power_df['Percent_Revenue'] = quarterly_power_df['Cost'] / (revenue_df['Revenue (M Dollars)'].values*1e6)

#Building regression models
cost_model = np.poly1d(np.polyfit(annual_power_df.index, annual_power_df['Cost'], deg=1))
cons_model = np.poly1d(np.polyfit(annual_power_df.index, annual_power_df['Consumption MW'], deg=1))
cost_pred = []
cost_pred.append(cost_model(6) * 0.7 + cons_model(6)*0.3*1e6)
cost_pred.append(cost_model(7) * 0.7 + cons_model(7)*0.3*0.03)
cost_pred.append(cost_model(8) * 0.7 + cons_model(8)*0.3*0.03)
print()
print("Three year prediction")
print("2025")
print(f"70 percent original cost: {cost_model(6) * 0.7}")
print(f"30 percent sustainability cost: {cons_model(6)*0.3*1e6}")
print(f"Total cost: {cost_pred[0]}")
print("2026")
print(f"70 percent original cost: {cost_model(7) * 0.7}")
print(f"30 percent sustainability cost: {cons_model(7)*0.3*0.03}")
print(f"Total cost: {cost_pred[1]}")
print("2027")
print(f"70 percent original cost: {cost_model(8) * 0.7}")
print(f"30 percent sustainability cost: {cons_model(8)*0.3*0.03}")
print(f"Total cost: {cost_pred[2]}")

#Plotting

plt.subplot(2, 2, 1)
plt.plot(range(len(cons_df)), cons_df['Consumption MW'])
plt.subplot(2, 2, 2)
plt.plot(range(len(priceRate_df)), priceRate_df['dollars per kW'])
plt.subplot(2, 2, 3)
plt.plot(range(len(revenue_df)), revenue_df['Revenue (M Dollars)'])
plt.title('Original Consumption, Rate, Revenue')

plt.figure()
top_three_months = monthly_power_df.sort_values(by='Cost', ascending=False).head(3)
plt.plot(monthly_power_df.index, monthly_power_df['Cost'])
plt.scatter(top_three_months.index, top_three_months['Cost'])
print()
print("Top three power costs")
print(top_three_months)
plt.title('Monthly Power Costs')

plt.figure()
plt.plot(annual_power_df.index, annual_power_df['Cost'])
print()
print("annual power metrics")
print(annual_power_df)
plt.title('Annual Power Costs')

plt.figure()
plt.plot(quarterly_power_df.index, quarterly_power_df['Percent_Revenue'])
top_three_quarters = quarterly_power_df.sort_values(by='Percent_Revenue', ascending=False).head(3)
plt.scatter(top_three_quarters.index, top_three_quarters['Percent_Revenue'])
print()
print("top three quarter metrics")
print(top_three_quarters)
print("Most recent quarter")
print(quarterly_power_df.iloc[-1])
plt.title('Percent of Revenue In Power by Quarter')

plt.figure()
plt.plot(range(len(cost_pred)), cost_pred)
plt.title('Power Cost Prediction 2025-2027')

plt.show()