from pandas import read_excel
from statsmodels.formula.api import ols
series = read_excel('MSTAdata_33276048_33347999_33270635.xlsx', 
                    sheet_name='data1', header=0,  squeeze=True, dtype=float)
                    


#reading the basic variables
MSTA = series.MSTA
CH4  = series.CH4 
GMAF = series.GMAF
ET12 = series.ET12

#reading the indicator variables
D1=series.D1
D2=series.D2
D3=series.D3
D4=series.D4
D5=series.D5
D6=series.D6
D7=series.D7
D8=series.D8
D9=series.D9
D10=series.D10
D11=series.D11

#Regression model(s)
formula = 'MSTA ~ CH4 + GMAF + ET12 + D1+D2+D3+D4+D5+D6+D7+D8+D9+D10+D11'


#Ordinary Least Squares (OLS)
results = ols(formula, data=series).fit()
print(results.summary())

# the two tables show the changes in the overall and 
# individual significance of the model when
# the indicator variables (Di, i=1, ..., 11) are added
# Pay attention to the changes in the key statistics 

# add 11 month indicator to the initial model 
