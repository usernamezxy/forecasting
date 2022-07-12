# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 14:18:09 2022

@author: Administrator
"""

# task2 ARIMA forecasting time plot
from pandas import read_excel
import matplotlib.pyplot as plt
series = read_excel('MSTAdata_33276048_33347999_33270635.xlsx', sheet_name='MSTA', header=0,
                    index_col=0, parse_dates=True, squeeze=True)
series.plot(color='red')
plt.xlabel('Dates')
plt.ylabel('MSTA')
plt.title('MSTA from 1850 to 2021')
plt.show()
