import pandas as pd
import matplotlib.pyplot as plt

analytics_df = pd.read_csv('website_data.csv')
sessions_df = pd.read_csv('web_sessions.csv')
web_df = analytics_df.copy()

dateSeries = sessions_df['MonthDay']+' ' + sessions_df['Year'].astype(str)
sessions_df['Date'] = pd.to_datetime(dateSeries)
sessions_df = sessions_df.sort_values('Date', ascending=False).reset_index(drop=True)
date_expansion = sessions_df['Date'].repeat(sessions_df['Visits'])
web_df['Date'] = date_expansion.reset_index(drop=True)

i=1
x=range(len(web_df['Date']))
for col in web_df.columns:
    plt.figure()
    plt.plot(web_df[col].iloc[::-1].reset_index(drop=True))
    plt.title(col)

plt.tight_layout()
plt.show()