# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 16:07:50 2022

@author: Administrator
"""

from pandas import read_excel
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from matplotlib import pyplot

series = read_excel('MSTAdata_33276048_33347999_33270635.xlsx', sheet_name='MSTA', usecols = [1], 
                             header=0, squeeze=True, dtype=float)

#  Seaonal difference
X = series.values
SeasDiff = list()
for i in range(12, len(X)):
	value = X[i] - X[i - 12]
	SeasDiff.append(value)
    
# Time, ACF, and PACF plots for the seasonally differenced series
pyplot.plot(SeasDiff)
pyplot.title('Time plot seasonally differenced series')
plot_acf(SeasDiff, title='ACF plot of seasonally differenced series', lags=50)
plot_pacf(SeasDiff, title='PACF plot of seasonally differenced series', lags=50)
pyplot.show()

# Seasonal + First difference
Y = SeasDiff
SeasFirstDiff = list()
for i in range(1, len(Y)):
	value = Y[i] - Y[i - 1]
	SeasFirstDiff.append(value)
pyplot.plot(SeasFirstDiff)
pyplot.title('Time plot seasonally + first differenced series')
plot_acf(SeasFirstDiff, title='ACF plot of seasonally + first differenced series', lags=50)
plot_pacf(SeasFirstDiff, title='PACF plot of seasonally + first differenced series', lags=50)
pyplot.show()
