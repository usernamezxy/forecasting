
from pandas import read_excel
from statsmodels.tsa.api import Holt
#from matplotlib import pyplot
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.formula.api import ols
series = read_excel('MSTAdata_33276048_33347999_33270635.xlsx', 
                    sheet_name='data1', header=0, squeeze=True, dtype=float)


#reading the basic variables
MSTA = series.MSTA
CH4  = series.CH4 
GMAF = series.GMAF
ET12 = series.ET12

# Forecasting for AAA using Holt's linear method
fit1 = Holt(CH4).fit(optimized=True)
fcast1 = fit1.forecast(33).rename("future trend")
fit1.fittedvalues.plot(color='red')
fcast1.plot(color='red', legend=True)
CH4.plot(color='black', legend=True)
plt.title('Forecast of CH4 with Holt linear method')
plt.show()

# Forecasting for Tto4 using Holt's linear method
fit2 = Holt(GMAF).fit(optimized=True)
fcast2 = fit2.forecast(33).rename("Afuture trend")
fit2.fittedvalues.plot(color='red')
fcast2.plot(color='red', legend=True)
GMAF.plot(color='black', legend=True)
plt.title('Forecast of GMAF with Holt linear method')
plt.show()

# Forecasting for D3to4 using Holt's linear method
fit3 = Holt(ET12).fit(smoothing_level=0.8, smoothing_slope=0.2, optimized=False)
#fit3 = Holt(D3to4).fit(optimized=True)
fcast3 = fit3.forecast(33).rename("future trend")
fit3.fittedvalues.plot(color='red')
fcast3.plot(color='red', legend=True)
ET12.plot(color='black', legend=True)
plt.title('Forecast of ET12 with Holt linear method')
plt.show()

# Building the regression based forecast for main variable, DEOM
# Regression model(s)
formula = 'MSTA ~ CH4 + GMAF + ET12'

# ols generate statistics and the parameters b0, b1, etc., of the model
results = ols(formula, data=series).fit()
results.summary()
b0 = results.params.Intercept
b1 = results.params.CH4
b2 = results.params.GMAF
b3 = results.params.ET12

# putting the fitted values of the forecasts of AAA, Tto4, and D3to4 in arrays
a1 = np.array(fit1.fittedvalues)
a2 = np.array(fit2.fittedvalues)
a3 = np.array(fit3.fittedvalues)

# Building the fitted part of the forecast of DEOM 
F=a1
for i in range(303):
    F[i] = b0 + a1[i]*b1 + a2[i]*b2 + a3[i]*b3

# putting the values of the forecasts of AAA, Tto4, and D3to4 in arrays
v1=np.array(fcast1)
v2=np.array(fcast2)
v3=np.array(fcast3)

# Building the 6 values of the forecast ahead
E=v1
for i in range(33):
    E[i] = b0 + v1[i]*b1 + v2[i]*b2 + v3[i]*b3


# Joining the fitted values of the forecast and the points ahead
K=np.append(F, E)

# Reading the original DEOM time series for all the 59 periods
MSTAfull0 = read_excel('MSTAdata_33276048_33347999_33270635.xlsx',
                       sheet_name='data3', header=0,  squeeze=True, dtype=float)

                   
###########################
# Evaluating the MSE to generate the confidence interval
MSTAfull = MSTAfull0.MSTAfull
values=MSTAfull[0:303]
Error = values - F
MSE=sum(Error**2)*1.0/len(F)

## Lower and upper bounds of forecasts for z=1.282; see equation (2.2) in Chap 2.
#LowerE = E - 1.282*MSE
#UpperE = E + 1.282*MSE

LowerE = MSTAfull0.LowerE
UpperE = MSTAfull0.UpperE
###############################
print(LowerE)
# Plotting the graphs of K and DEOMfull with legends
from matplotlib.legend_handler import HandlerLine2D

line1, = plt.plot(K, color='red', label='Forecast values')
line2, = plt.plot(MSTAfull, color='black', label='Original data')
line3, = plt.plot(LowerE, color='blue', label='Lower forecast')
line4, = plt.plot(UpperE, color='orange', label='Upper forecast')
plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
plt.title('MSTA regression forecast with confidence interval')
plt.show()

# Proceeding as as in other demos, forecasts
# can be generated for other scenarios; i.e., with different combinations of va














