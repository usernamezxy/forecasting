import pandas as pd
from matplotlib import pyplot
#MSTA after truncating
series_MSTA = pd.read_excel('MSTAdata_33276048_33347999_33270635.xlsx',sheet_name='new', header=0, index_col=0,usecols=['Time','MSTA'],parse_dates=True)  
series_MSTA.plot(title='MSTA Original Data')

#MSTA after calendar adjustments
series_MSTA_ad = pd.read_excel('MSTAdata_33276048_33347999_33270635.xlsx',sheet_name='new', header=0, index_col=0,usecols=['Time','Adjusted MSTA'],parse_dates=True)  
series_MSTA_ad.plot(title='MSTA Adjusted Data')

#MSTA seasonal plot
series_MSTA_seas = pd.read_excel('MSTAdata_33276048_33347999_33270635.xlsx',sheet_name='SeasData1', header=0, index_col=0,parse_dates=True, squeeze=True)  
series_MSTA_seas.plot(title='MSTA Seasonal Plot')

#HW prediction
from statsmodels.tsa.api import ExponentialSmoothing

#set the frequency of the data time index as Monthly start as indicated by the data
series_MSTA.index.freq='MS'
#MSTA model 1 with additive trend effect and additive seasonal effect
series_MSTA['forecasting1'] = ExponentialSmoothing(series_MSTA['MSTA'],trend='add',seasonal='add',seasonal_periods=12,initialization_method='estimated').fit(smoothing_level = 0.3, smoothing_trend=0.5,  smoothing_seasonal=0.7).fittedvalues
series_MSTA[['MSTA','forecasting1']].plot(title='MSTA Holt Winters:Addictive Trend')
fit_MSTA1=ExponentialSmoothing(series_MSTA['MSTA'],trend='add',seasonal='add',seasonal_periods=12,initialization_method='estimated').fit(smoothing_level = 0.3, smoothing_trend=0.5,  smoothing_seasonal=0.7)

#MSTA model 2 with additive trend effect and additive seasonal effect(optimized)
series_MSTA['forecasting2'] = ExponentialSmoothing(series_MSTA['MSTA'],trend='add',seasonal='add',seasonal_periods=12,initialization_method='estimated').fit().fittedvalues
series_MSTA[['MSTA','forecasting2']].plot(title='MSTA Holt Winters:Addictive Trend')
fit_MSTA2=ExponentialSmoothing(series_MSTA['MSTA'],trend='add',seasonal='add',seasonal_periods=12,initialization_method='estimated').fit()

#====================================
# Evaluating the errors 
#====================================
from sklearn.metrics import mean_squared_error 
MSE_MSTA1=mean_squared_error(series_MSTA['forecasting1'],series_MSTA['MSTA'])
MSE_MSTA2=mean_squared_error(series_MSTA['forecasting2'],series_MSTA['MSTA'])

#=====================================
# Printing the paramters and errors for each scenario
#=====================================
results=pd.DataFrame(index=[r"alpha", r"beta", r"gamma", r"l0", "b0", "MSE"])
params = ['smoothing_level', 'smoothing_trend', 'smoothing_seasonal', 'initial_level', 'initial_trend']
results["MSTA model 1"] = [fit_MSTA1.params[p] for p in params] + [MSE_MSTA1]
results["MSTA model 2"] = [fit_MSTA2.params[p] for p in params] + [MSE_MSTA2]
print(results)

#=====================================
# Evaluating and plotting the residual series for each scenario
#=====================================
MSTA_residuals1= fit_MSTA1.fittedvalues - series_MSTA['MSTA']
MSTA_residuals2= fit_MSTA2.fittedvalues - series_MSTA['MSTA']

MSTA_residuals1.rename('residual plot for MSTA model 1').plot(color='red', legend=True,title='Residual Plot for MSTA Model 1')
MSTA_residuals2.rename('residual plot for MSTA model 2').plot(color='blue', legend=True,title='Residual Plot for MSTA Model 2')
pyplot.show()

#=====================================
# ACF plots of the residual series for each scenario
#=====================================
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(MSTA_residuals1, title='Residual ACF for MSTA model 1', lags=50)
plot_acf(MSTA_residuals2, title='Residual ACF for MSTA model 2', lags=50)
pyplot.show()
