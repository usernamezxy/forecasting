import pandas as pd
from matplotlib import pyplot

#CH4 after truncating
series_CH4 = pd.read_excel('CH4data_33276048_33347999_33270635.xlsx', sheet_name='AdjustedData',header=0, index_col=0,usecols=['year','CH4'],parse_dates=True)
series_CH4.plot(title='CH4 Original Data')

#CH4 after calendar adjustments
series_CH4_ad = pd.read_excel('CH4data_33276048_33347999_33270635.xlsx',sheet_name='AdjustedData', header=0, index_col=0,usecols=['year','Adjusted CH4'],parse_dates=True)  
series_CH4_ad.plot(title='CH4 Adjusted Data')

#CH4 seasonal plot
series_CH4_seas = pd.read_excel('CH4data_33276048_33347999_33270635.xlsx', sheet_name='SeasData1',header=0, index_col=0, parse_dates=True, squeeze=True)
series_CH4_seas.plot(title='CH4 Seasonal Plot')

#HW prediction
from statsmodels.tsa.api import ExponentialSmoothing

#set the frequency of the data time index as Monthly start as indicated by the data
series_CH4.index.freq='MS'
#MSTA model 1 with additive trend effect and no seasonal effect
series_CH4['forecasting1'] = ExponentialSmoothing(series_CH4['CH4'],trend='add',initialization_method='estimated').fit(smoothing_level = 0.3, smoothing_trend=0.5).fittedvalues
series_CH4[['CH4','forecasting1']].plot(title='CH4 Holt Winters Linear Exponential Smoothing')
fit_CH41=ExponentialSmoothing(series_CH4['CH4'],trend='add',initialization_method='estimated').fit(smoothing_level = 0.3, smoothing_trend=0.5)

#CH4 model 2 with additive trend effect and no seasonal effect(optimized)
series_CH4['forecasting2'] = ExponentialSmoothing(series_CH4['CH4'],trend='add',initialization_method='estimated').fit().fittedvalues
series_CH4[['CH4','forecasting2']].plot(title='CH4 Holt Winters Linear Exponential Smoothing(optimized)')
fit_CH42=ExponentialSmoothing(series_CH4['CH4'],trend='add',initialization_method='estimated').fit()

#====================================
# Evaluating the errors 
#====================================
from sklearn.metrics import mean_squared_error 

MSE_CH41=mean_squared_error(series_CH4['forecasting1'],series_CH4['CH4'])
MSE_CH42=mean_squared_error(series_CH4['forecasting2'],series_CH4['CH4'])

#=====================================
# Printing the paramters and errors for each scenario
#=====================================
results=pd.DataFrame(index=[r"alpha", r"beta", r"gamma", r"l0", "b0", "MSE"])
params = ['smoothing_level', 'smoothing_trend', 'smoothing_seasonal', 'initial_level', 'initial_trend']
results["CH4 model 1"] = [fit_CH41.params[p] for p in params] + [MSE_CH41]
results["CH4 model 2"] = [fit_CH42.params[p] for p in params] + [MSE_CH42]
print(results)

#=====================================
# Evaluating and plotting the residual series for each scenario
#=====================================
CH4_residuals1= fit_CH41.fittedvalues - series_CH4['CH4']
CH4_residuals2= fit_CH42.fittedvalues - series_CH4['CH4']

CH4_residuals1.rename('residual plot for CH4 model 1').plot(color='green', legend=True,title='Residual Plot for CH4 Model 1')
CH4_residuals2.rename('residual plot for CH4 model 2').plot(color='black', legend=True,title='Residual Plot for CH4 Model 2')
pyplot.show()

#=====================================
# ACF plots of the residual series for each scenario
#=====================================
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(CH4_residuals1, title='Residual ACF for CH4 model 1', lags=50)
plot_acf(CH4_residuals2, title='Residual ACF for CH4 model 2', lags=50)
pyplot.show()