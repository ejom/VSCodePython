import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy import sin, cos, pi

#Clean open_data csv file
df_open = pd.read_csv('Open_Data_Website_Traffic.csv')

df_open['Sessions'] = df_open[['Socrata Sessions', 'Geohub Sessions']].sum(axis=1)
df_open['Bounce Rate'] = df_open[['Socrata Bounce Rate', 'Geohub Bounce Rate']].mean(axis=1)

summedUsers = df_open[['Socrata Users', 'Geohub Users']].sum(axis=1)
df_open['Users'] = df_open['Combined Users'].fillna(summedUsers)

df_soc_geo = df_open[['Date', 'Sessions', 'Bounce Rate', 'Users']].copy()
df_soc_geo['datetime'] = pd.to_datetime(df_open['Date'])

df_SocGeo_full = df_soc_geo.sort_values(by='datetime').reset_index()
df_SocGeo = df_SocGeo_full[df_SocGeo_full['datetime'].between('2017-01-01', '2018-09-11')]

#Import the already clean dailyLA_web.csv
df_la = pd.read_csv('dailyLA_clean.csv')

def plotControlChart(df, val):
    plt.xticks([])
    plt.plot(df['datetime'], df[val], label=val)
    #Analyze control line metrics
    df_mean = df[val].mean()
    df_std = df[val].std()
    CL = df_mean
    UCL = df_mean + 3*df_std
    LCL = df_mean - 3*df_std
    print(f"Center Line: {df_mean}")
    print(f"Upper Line: {df_mean + 3*df_std}")
    print(f"Lower Line: {df_mean - 3*df_std}")
    print(df[(df[val]>=UCL) | (df[val]<=LCL)])
    print()
    plt.axhline(y=(CL), color='black')
    plt.axhline(y=(UCL), color='black')
    plt.axhline(y=(LCL), color='black')

#Plot sessions, bounce rate, and users side by side for both datasets
plt.subplot(2, 2, 1)
print("Socrota and Geohub Users metrics:")
plotControlChart(df_SocGeo, 'Users')
plt.title('Socrata and Geohub Users')
plt.subplot(2, 2, 2)
print("Socrota and Geohub Bounce Rate metrics:")
plotControlChart(df_SocGeo, 'Bounce Rate')
plt.title('Socrata and Geohub Bounce Rate')

plt.subplot(2, 2, 3)
print("LA Users metrics:")
plotControlChart(df_la, 'Users')
plt.title('LA Users')
plt.subplot(2, 2, 4)
print("LA Bounce Rate metrics:")
plotControlChart(df_la, 'Bounce Rate')
plt.title('LA Bounce Rate')

#Split LA_web data 2014-2015 and 2026 and up. 
"""
cutoff_date = '2015-12-31'
df_la_small = df_la[df_la['datetime'] <= cutoff_date].copy()
df_la_big = df_la[df_la['datetime'] > cutoff_date].copy()

#Plot small LA web
plt.subplot(3, 2, 3)
print("LA Pre Merge Users metrics:")
plotControlChart(df_la_small, 'Users')
plt.title('LA Sessions and Users before merge')

plt.subplot(3, 2, 4)
print("LA Pre Merge Bounce Rate metrics:")
plotControlChart(df_la_small, 'Bounce Rate')
plt.title('LA Bounce Rate before merge')

#Plot big LA vals
plt.subplot(3, 2, 5)
print("LA Post Merge Users metrics:")
plotControlChart(df_la_big, 'Users')
plt.title('LA Sessions and Users after merge')
plt.ylim(top=2.5e6)

plt.subplot(3, 2, 6)
print("LA Post Merge Bounce Rate metrics:")
plotControlChart(df_la_big, 'Bounce Rate')
plt.title('LA Bounce Rate after merge')
"""

plt.figure()

#Analyze variability of most recent data:
def analyze_when_in_control(df, val):
    df_rev = df.iloc[::-1].copy()
    df_rev['CumMean'] = df_rev[val].expanding().mean()
    df_rev['CumSTD'] = df_rev[val].expanding().std().fillna(0)
    df_rev['Upper Bound'] = df_rev['CumMean'] + 3*df_rev['CumSTD']
    df_rev['Lower Bound'] = df_rev['CumMean'] - 3*df_rev['CumSTD']

    df_rev['Window_Max'] = df_rev[val].expanding().max()
    df_rev['Window_Min'] = df_rev[val].expanding().min()

    in_bounds_rev = (df_rev['Window_Max'] <= df_rev['Upper Bound']) & (df_rev['Window_Min'] >= df_rev['Lower Bound'])
    in_control_rev = in_bounds_rev.cummin()

    in_control_mask_rev = in_control_rev.cummin()
    df_in_control_rev = df_rev[in_control_mask_rev]
    df_in_control = df_in_control_rev.iloc[::-1].reset_index()

    return df_in_control

plt.subplot(2, 2, 1)
print("Analyzing SocGeo Recent Users")
df_SocGeo_conUsers = analyze_when_in_control(df_SocGeo, 'Users')
plotControlChart(df_SocGeo_conUsers, 'Users')
plt.title('Recent SocGeo Users in control')
print(f"Date process begins to be in control: {df_SocGeo_conUsers['Date'].iloc[0]}")
print()

plt.subplot(2, 2, 2)
print("Analyzing SocGeo Recent Bounce Rate")
df_SocGeo_conBounce = analyze_when_in_control(df_SocGeo, 'Bounce Rate')
plotControlChart(df_SocGeo_conBounce, 'Bounce Rate')
plt.title('Recent SocGeo Bounce Rate in control')
print(f"Date process begins to be in control: {df_SocGeo_conBounce['Date'].iloc[0]}")
print()

plt.subplot(2, 2, 3)
print("Analyzing LA Recent Users")
df_la_conUsers = analyze_when_in_control(df_la, 'Users')
plotControlChart(df_la_conUsers, 'Users')
plt.title('Recent LA Users in control')
print(f"Date process begins to be in control: {df_la_conUsers['datetime'].iloc[0]}")
print()

plt.subplot(2, 2, 4)
print("Analyzing LA Recent Bounce Rate")
df_la_conBounce = analyze_when_in_control(df_la, 'Bounce Rate')
plotControlChart(df_la_conBounce, 'Bounce Rate')
plt.title('Recent LA Bounce Rate in control')
print(f"Date process begins to be in control: {df_la_conBounce['datetime'].iloc[0]}")
print()

plt.show()

"""
plt.subplot(3, 2, 3)
print("Analyzing LA Pre Merge Recent Users")
df_la_small_conUsers = analyze_when_in_control(df_la_small, 'Users')
plotControlChart(df_la_small_conUsers, 'Users')
plt.title('Recent LA Pre Merge Users in control')
print(f"Date process begins to be in control: {df_la_small_conUsers['datetime'].iloc[0]}")
print()

plt.subplot(3, 2, 4)
print("Analyzing LA Pre Merge Recent Bounce Rates")
df_la_small_conBounce = analyze_when_in_control(df_la_small, 'Bounce Rate')
plotControlChart(df_la_small_conBounce, 'Bounce Rate')
plt.title('Recent LA Pre Merge Bounce Rates in control')
print(f"Date process begins to be in control: {df_la_small_conBounce['datetime'].iloc[0]}")
print()

plt.subplot(3, 2, 5)
print("Analyzing LA Post Merge Recent Users")
df_la_big_conUsers = analyze_when_in_control(df_la_big, 'Users')
plotControlChart(df_la_big_conUsers, 'Users')
plt.title('Recent LA Post Merge Users in control')
print(f"Date process begins to be in control: {df_la_big_conUsers['datetime'].iloc[0]}")
print()

plt.subplot(3, 2, 6)
print("Analyzing LA Post Merge Recent Bounce Rates")
df_la_big_conBounce = analyze_when_in_control(df_la_big, 'Bounce Rate')
plotControlChart(df_la_big_conBounce, 'Bounce Rate')
plt.title('Recent LA Post Merge Bounce Rates in control')
print(f"Date process begins to be in control: {df_la_big_conBounce['datetime'].iloc[0]}")
print()
"""
