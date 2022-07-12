
from pandas import read_excel
from statsmodels.formula.api import ols
series = read_excel('MSTAdata_33276048_33347999_33270635.xlsx', 
                    sheet_name='data1', header=0,  squeeze=True, dtype=float)
                    

#reading the basic variables
MSTA = series.MSTA
CH4  = series.CH4 

GMAF = series.GMAF
ET12 = series.ET12

#Regression model(s)
formula = 'MSTA ~ CH4 + GMAF + ET12'

#Ordinary Least Squares (OLS)
results = ols(formula, data=series).fit()
print(results.summary())

# Here the main table is the first one,
# where the main statistics are the R-squared (line 1)
# and the P-value; i.e., Prob (F-statistic)
