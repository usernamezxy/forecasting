# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 15:43:30 2022

@author: Administrator
"""

from pandas import read_excel
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
series = read_excel('MSTAdata_33276048_33347999_33270635.xlsx',  sheet_name='MSTA', usecols = [1], 
                             header=0, squeeze=True, dtype=float) 
# ACF plot on 50 time lags
plot_acf(series, title='ACF of MSTA', lags=50)

# PACF plot on 50 time lags
plot_pacf(series, title='PACF of MSTA', lags=50)
pyplot.show()