#imports
import yfinance as yf
import numpy as np
import pandas as pd
import hvplot.pandas
import holoviews as hv
from holoviews import dim, opts
import matplotlib.pyplot as plt #show function for graph
hv.extension('bokeh', 'matplotlib')
pd.options.plotting.backend = 'holoviews'
from datetime import timedelta #Find difference in dates
from bokeh.models.formatters import DatetimeTickFormatter #Formatting the dates so they can be plotted.
from bokeh.io import export_png

today = pd.to_datetime('now').normalize()
days = 90

def date_difference(date, days):
    subtracted_date = pd.to_datetime(date) - timedelta(days=days)
    subtracted_date = subtracted_date.strftime("%Y-%m-%d")

    return subtracted_date


#Start date for algo
start = date_difference(today, days)

#Yahoo Finance API
data = yf.download("FINSX MEIIX", start=start, end=today)

#Drop all colmns besides "Adj Close"
data["Adj Close"] = data["Adj Close"]
data = pd.DataFrame(data)
data = data.drop(columns=["Close","High","Low","Open","Volume"])

#Clean up data
data['FINSX']= data['Adj Close']['FINSX']
data['MEIIX']= data['Adj Close']['MEIIX']

data_set = data.drop(columns = ["Adj Close"])
data.head()

#Bollinger Bands - 2 Standard Deviation from the average.
data_set['FINSX UB'] = data_set['FINSX'].rolling(window = 90, min_periods=1).mean() + data_set['FINSX'].rolling(window = 90, min_periods=1).std() * 2
data_set['FINSX LB'] = data_set['FINSX'].rolling(window = 90, min_periods=1).mean() - data_set['FINSX'].rolling(window = 90, min_periods=1).std() * 2
data_set['MEIIX UB'] = data_set['MEIIX'].rolling(window = 90, min_periods=1).mean() + data_set['MEIIX'].rolling(window = 90, min_periods=1).std() * 2
data_set['MEIIX LB'] = data_set['MEIIX'].rolling(window = 90, min_periods=1).mean() - data_set['MEIIX'].rolling(window = 90, min_periods=1).std() * 2

data_set = data_set.dropna()

data_set.reset_index(inplace=True)

Date=[]
FINSX = []
MEIIX = []
FINSX_UB = []
FINSX_LB = []
MEIIX_UB = []
MEIIX_LB = []


for x in data_set['Date']:
    Date.append(x)
    
for x in data_set['FINSX']:
    FINSX.append(x)
    
for x in data_set['MEIIX']:
    MEIIX.append(x)
    
for x in data_set['FINSX UB']:
    FINSX_UB.append(x)
    
for x in data_set['FINSX LB']:
    FINSX_LB.append(x)
    
for x in data_set['MEIIX UB']:
    MEIIX_UB.append(x)
    
for x in data_set['MEIIX LB']:
    MEIIX_LB.append(x)

    
#Create new dataframes
Date = pd.DataFrame(Date)
FINSX = pd.DataFrame(FINSX)
MEIIX = pd.DataFrame(MEIIX)
FINSX_UB = pd.DataFrame(FINSX_UB)
FINSX_LB = pd.DataFrame(FINSX_LB)
MEIIX_UB = pd. DataFrame(MEIIX_UB)
MEIIX_LB = pd. DataFrame(MEIIX_LB)

#Join the new datasets together
new_df = pd.concat([Date, FINSX, MEIIX, FINSX_UB, FINSX_LB, MEIIX_UB, MEIIX_LB], axis=1)

#Create new/appropriate column names
new_df.columns = ['Date', 'FINSX', 'MEIIX', 'FINSX_UB', 'FINSX_LB', 'MEIIX_UB', 'MEIIX_LB']

#Visual Representation of FINSX
FINSX_plot = new_df.hvplot.line(x="Date", y=['FINSX','FINSX_UB','FINSX_LB'], value_label = 'Fidelity Advisor New Insights Fund Class I')

#Visual Representation of MEIIX
MEIIX_plot = new_df.hvplot.line(x="Date", y=['MEIIX','MEIIX_UB','MEIIX_LB'], value_label = 'MFS Value Fund Class I')

#FINSX UB/LB Crossover
new_df['FINSX_LB_Cross'] = np.where(new_df['FINSX'] <= new_df['FINSX_LB'], int('1'), int('0'))
new_df['FINSX_UB_Cross'] = np.where(new_df['FINSX'] >= new_df['FINSX_UB'], int('1'), int('0'))

#MEIIX UB/LB Crossover

new_df['MEIIX_LB_Cross'] = np.where(new_df['MEIIX'] <= new_df['MEIIX_LB'], int('1'), int('0'))
new_df['MEIIX_UB_Cross'] = np.where(new_df['MEIIX'] >= new_df['MEIIX_UB'], int('1'), int('0'))

new_df_2 = new_df.copy()

#For loop to add the appropriate info to a DF so it can be emailed out.

Date_FINSX_UB = []
Date_FINSX_LB = []
Upper_Bound_FINSX = []
Lower_Bound_FINSX = []
Current_Price_FINSX_UB = []
Current_Price_FINSX_LB = []

for index, column in new_df_2.iterrows():
    if new_df_2.loc[index,'FINSX_LB_Cross'] == 1:
        print(new_df_2.loc[index])
        
#For loop to add the appropriate info to a DF so it can be emailed out.
#LB FINSX

for index, column in new_df_2.iterrows():
    if new_df_2.loc[index,'FINSX_LB_Cross'] == 1:
        Date_FINSX_LB.append(new_df_2.loc[index, 'Date'])
        Lower_Bound_FINSX.append(new_df_2.loc[index, 'FINSX_LB'])
        Current_Price_FINSX_LB.append(new_df_2.loc[index, 'FINSX'])


output_FINSX_LB = pd.DataFrame({"Date": Date_FINSX_LB, "Lower Bound": Lower_Bound_FINSX, "PRICE - FINSX": Current_Price_FINSX_LB})
FINSX_LB_last_two_values = output_FINSX_LB.iloc[-2:,:]

#For loop to add the appropriate info to a DF so it can be emailed out.
#UB FINSX

for index, column in new_df_2.iterrows():
    if new_df_2.loc[index,'FINSX_UB_Cross'] == 1:
        Date_FINSX_UB.append(new_df_2.loc[index, 'Date'])
        Upper_Bound_FINSX.append(new_df_2.loc[index, 'FINSX_UB'])
        Current_Price_FINSX_UB.append(new_df_2.loc[index, 'FINSX'])
        
output_FINSX_UB = pd.DataFrame({"Date": Date_FINSX_UB, "Upper Bound": Upper_Bound_FINSX, "PRICE - FINSX": Current_Price_FINSX_UB})
FINSX_UB_last_two_values = output_FINSX_UB.iloc[-2:,:]

#MEIIX

Date_MEIIX_UB = []
Date_MEIIX_LB = []
Upper_Bound_MEIIX = []
Lower_Bound_MEIIX = []
Current_Price_MEIIX_UB = []
Current_Price_MEIIX_LB = []

for index, column in new_df_2.iterrows():
    if new_df_2.loc[index,'MEIIX_UB_Cross'] == 1:
        Date_MEIIX_UB.append(new_df_2.loc[index, 'Date'])
        Upper_Bound_MEIIX.append(new_df_2.loc[index, 'MEIIX_UB'])
        Current_Price_MEIIX_UB.append(new_df_2.loc[index, 'MEIIX'])
        
output_MEIIX_UB = pd.DataFrame({"Date": Date_MEIIX_UB, "Upper Bound": Upper_Bound_MEIIX, "PRICE - MEIIX": Current_Price_MEIIX_UB})
MEIIX_UB_last_two_values = output_MEIIX_UB.iloc[-2:,:]

for index, column in new_df_2.iterrows():
    if new_df_2.loc[index,'MEIIX_LB_Cross'] == 1:
        Date_MEIIX_LB.append(new_df_2.loc[index, 'Date'])
        Lower_Bound_MEIIX.append(new_df_2.loc[index, 'MEIIX_LB'])
        Current_Price_MEIIX_LB.append(new_df_2.loc[index, 'MEIIX'])
        
output_MEIIX_LB = pd.DataFrame({"Date": Date_MEIIX_LB, "Lower Bound": Lower_Bound_MEIIX, "PRICE - MEIIX": Current_Price_MEIIX_LB})

MEIIX_LB_last_two_values = output_MEIIX_LB.iloc[-2:,:]

MEIIX_LB_CSV =  MEIIX_LB_last_two_values.to_csv('MEIIX_LB_last_two_values.csv', index = None, header = True)

from bokeh.io import export_svg

plot_1 = hv.render(MEIIX_plot)
export_png(plot_1, filename = "plot_MEIIX.png")

plot_2 = hv.render(FINSX_plot)
export_png(plot_2, filename = "plot_FINSX.png")