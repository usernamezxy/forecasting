import pandas as pd
from matplotlib import pyplot

#ET12 original data
series_ET12 = pd.read_excel('ET12data_33276048_33347999_33270635.xlsx', sheet_name='AdjustedData',header=0, index_col=0,usecols=['year','ET12'],parse_dates=True)
series_ET12.plot(title='ET12 Original Data')

#ET12 after calendar adjustments
series_ET12_ad = pd.read_excel('ET12data_33276048_33347999_33270635.xlsx', sheet_name='AdjustedData',header=0, index_col=0,usecols=['year','Adjusted ET12'],parse_dates=True)
series_ET12_ad.plot(title='ET12 Adjusted Data')

#ET12 seasonal plot
series_ET12_seas = pd.read_excel('ET12data_33276048_33347999_33270635.xlsx', sheet_name='SeasData1',header=0, index_col=0,parse_dates=True)
series_ET12_seas.plot(title='ET12 Seasonal Plot')

#HW prediction
from statsmodels.tsa.api import ExponentialSmoothing

#set the frequency of the data time index as Monthly start as indicated by the data
series_ET12.index.freq='MS'
#ET12 model 1 with additive trend effect and additive seasonal effect
series_ET12['forecasting1'] = ExponentialSmoothing(series_ET12['ET12'],trend='add',seasonal='add',seasonal_periods=12,initialization_method='estimated').fit(smoothing_level = 0.3, smoothing_trend=0.5,smoothing_seasonal=0.7).fittedvalues
series_ET12[['ET12','forecasting1']].plot(title='HW method-based forecasts for ET12')
fit_ET121=ExponentialSmoothing(series_ET12['ET12'],trend='add',seasonal='add',seasonal_periods=12,initialization_method='estimated').fit(smoothing_level = 0.3, smoothing_trend=0.5,smoothing_seasonal=0.7)

#ET12 model 2 with additive trend effect and additive seasonal effect(optimized)
series_ET12['forecasting2'] = ExponentialSmoothing(series_ET12['ET12'],trend='add',seasonal='add',seasonal_periods=12,initialization_method='estimated').fit().fittedvalues
series_ET12[['ET12','forecasting2']].plot(title='HW method-based forecasts for ET12(optimized)')
fit_ET122=ExponentialSmoothing(series_ET12['ET12'],trend='add',seasonal='add',seasonal_periods=12,initialization_method='estimated').fit()

#====================================
# Evaluating the errors 
#====================================
from sklearn.metrics import mean_squared_error 

MSE_ET121=mean_squared_error(series_ET12['forecasting1'],series_ET12['ET12'])
MSE_ET122=mean_squared_error(series_ET12['forecasting2'],series_ET12['ET12'])

#=====================================
# Printing the paramters and errors for each scenario
#=====================================
results=pd.DataFrame(index=[r"alpha", r"beta", r"gamma", r"l0", "b0", "MSE"])
params = ['smoothing_level', 'smoothing_trend', 'smoothing_seasonal', 'initial_level', 'initial_trend']
results["ET12 model 1"] = [fit_ET121.params[p] for p in params] + [MSE_ET121]
results["ET12 model 2"] = [fit_ET122.params[p] for p in params] + [MSE_ET122]
print(results)

#=====================================
# Evaluating and plotting the residual series for each scenario
#=====================================
ET12_residuals1= fit_ET121.fittedvalues - series_ET12['ET12']
ET12_residuals2= fit_ET122.fittedvalues - series_ET12['ET12']

ET12_residuals1.rename('residual plot for ET12 model 1').plot(color='pink', legend=True,title='Residual Plot for ET12 Model 1')
ET12_residuals2.rename('residual plot for ET12 model 2').plot(color='orange', legend=True,title='Residual Plot for ET12 Model 2')
pyplot.show()

#=====================================
# ACF plots of the residual series for each scenario
#=====================================
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(ET12_residuals1, title='Residual ACF for ET12 model 1', lags=50)
plot_acf(ET12_residuals2, title='Residual ACF for ET12 model 2', lags=50)
pyplot.show()