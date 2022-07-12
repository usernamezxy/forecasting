# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 21:37:38 2022

@author: Administrator
"""

from pandas import read_excel
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm  
plt.style.use('fivethirtyeight')

#==================================================================
#Loading the data set
df = read_excel('MSTAdata_33276048_33347999_33270635.xlsx',  sheet_name='MSTA', header=0, 
                index_col=0, parse_dates=True, squeeze=True)
#==================================================================

#==================================================================
#Fitting the ARIMA model and printing related statistics
# ARIMA(1, 1, 1)(1,1,1)12 in this case; 
#this one is based on AR1MA1 model template
mod = sm.tsa.statespace.SARIMAX(df, order=(1,1,1), seasonal_order=(1,0,1,12))
results = mod.fit(disp=False)
print(results.summary())
#==================================================================

#GRAPH BLOCK1======================================================
#Printing the graphical statistics of model (correlogram = ACF plot)
results.plot_diagnostics(figsize=(15, 12))
plt.show() 
#==================================================================

#GRAPH BLOCK2======================================================
# printing the part of forecasts fitted to original data (for accuracy evaluation)
# the start date has to be provided; hence should be a time within the original time series;
# in this case, it is to start on January 2000
pred = results.get_prediction(start=pd.to_datetime('2000-01'), dynamic=False)
pred_ci = pred.conf_int()

# printing one-step ahead forecasts together with the original data set;
# hence, the starting point (year) of the data set is required 
# in order to build the plot of original series
ax = df['1850':].plot(label='Original data')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7) 
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
plt.legend()
plt.show()
#===================================================================

#GRAPH BLOCK3=======================================================
# Get forecast 12 steps ahead in future
pred_uc = results.get_forecast(steps=12)
# Get confidence intervals of forecasts
pred_ci = pred_uc.conf_int()
# plotting forecasts ahead
ax = df.plot(label='Original data')
pred_uc.predicted_mean.plot(ax=ax, label='Forecast values', title='Forecast plot with confidence interval')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
plt.legend()
plt.show()
print(pred_ci)
#====================================================================

#====================================================================
# MSE evaluation
y_forecasted = pred.predicted_mean
y_truth = df['2000-01':]
# Compute the mean square error
MSE = ((y_forecasted - y_truth) ** 2).mean()
print('MSE of the forecasts is {}'.format(round(MSE, 2)))
#====================================================================