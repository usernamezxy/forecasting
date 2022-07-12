import pandas as pd
from matplotlib import pyplot

#GMAF after truncating
series_GMAF = pd.read_excel('GMAFdata_33276048_33347999_33270635.xlsx',sheet_name='AdjustedData', header=0, index_col=0,usecols=[0,2],parse_dates=True)
series_GMAF.plot(title='GMAF Original Data')

#GMAF after calendar adjustments
series_GMAF_ad = pd.read_excel('GMAFdata_33276048_33347999_33270635.xlsx', sheet_name='AdjustedData',header=0, index_col=0, usecols=['year','Adjusted GMAF'],parse_dates=True)
series_GMAF_ad.plot(title='GMAF Adjusted Data')

#GMAF seasonal plot
series_GMAF_seas = pd.read_excel('GMAFdata_33276048_33347999_33270635.xlsx', sheet_name='SeasData1',header=0, index_col=0, parse_dates=True, squeeze=True)
series_GMAF_seas.plot(title='GMAF Seasonal Plot')

#HW prediction
from statsmodels.tsa.api import ExponentialSmoothing

#set the frequency of the data time index as Monthly start as indicated by the data
series_GMAF.index.freq='MS'

#GMAF model with additive trend effect and multiplicative seasonal effect(optimized)
series_GMAF['forecasting'] = ExponentialSmoothing(series_GMAF['GMAF'],trend='add',seasonal='mul',seasonal_periods=12,initialization_method='estimated').fit().fittedvalues
series_GMAF[['GMAF','forecasting']].plot(title='HW method-based forecasts for GMAF')
fit_GMAF=ExponentialSmoothing(series_GMAF['GMAF'],trend='add',seasonal='mul',seasonal_periods=12,initialization_method='estimated').fit()

#====================================
# Evaluating the errors 
#====================================
from sklearn.metrics import mean_squared_error 

MSE_GMAF=mean_squared_error(series_GMAF['forecasting'],series_GMAF['GMAF'])

#=====================================
# Printing the paramters and errors for each scenario
#=====================================
results=pd.DataFrame(index=[r"alpha", r"beta", r"gamma", r"l0", "b0", "MSE"])
params = ['smoothing_level', 'smoothing_trend', 'smoothing_seasonal', 'initial_level', 'initial_trend']
results["GMAF model"] = [fit_GMAF.params[p] for p in params] + [MSE_GMAF]
print(results)

#=====================================
# Evaluating and plotting the residual series for each scenario
#=====================================
GMAF_residuals= fit_GMAF.fittedvalues - series_GMAF['GMAF']
GMAF_residuals.rename('residual plot for GMAF model').plot(color='purple', legend=True,title='Residual Plot for GMAF Model')
pyplot.show()

#=====================================
# ACF plots of the residual series for each scenario
#=====================================
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(GMAF_residuals, title='Residual ACF for GMAF model', lags=50)
pyplot.show()