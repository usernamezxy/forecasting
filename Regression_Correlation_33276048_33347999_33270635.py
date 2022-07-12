
from pandas import read_excel
import matplotlib.pyplot as plt
import pandas as pd
series = read_excel('MSTAdata_33276048_33347999_33270635.xlsx', sheet_name='data2', header=0, 
                      dtype=float)

#Plotting the scatter plots of each variable against the other one
pd.plotting.scatter_matrix(series, figsize=(8, 8))
plt.show()

# Correlation matrix for all the variables, 2 by 2
CorrelationMatrix = series.corr()
print(CorrelationMatrix)
# As in the case of Demo 1.4, corrcoef can be used for the variables in couples.