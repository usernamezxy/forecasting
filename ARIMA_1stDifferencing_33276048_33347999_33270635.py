# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 15:56:54 2022

@author: Administrator
"""

## detrend a time series using differencing
from pandas import read_excel
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from matplotlib import pyplot

series = read_excel('MSTAdata_33276048_33347999_33270635.xlsx',  sheet_name='MSTA', usecols = [1], 
                             header=0, squeeze=True, dtype=float) 
X = series.values
diff = list()
for i in range(1, len(X)):
	value = X[i] - X[i - 1]
	diff.append(value)
pyplot.plot(diff)
pyplot.title('Time plot MSTA 1st difference')

# ACF plot of time series
plot_acf(diff, title='ACF of MSTA 1st difference', lags=50)

# PACF plot of time series
plot_pacf(diff, title='PACF of MSTA 1st difference', lags=50)
pyplot.show()