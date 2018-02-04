import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import math
path='C:\\Users\\Administrator\\Desktop\\test\\od_test\\shanghai\\test_results\\0.05\\modeldis1_10000_1_0.5_home.csv'
df=pd.read_csv(path)
df=df[(df['model_value']!=0) & df['flux']!=0]
df['model_value']=df['model_value'].apply(math.log)
df['flux']=df['flux'].apply(math.log)
model=LinearRegression()
predict=model.fit(np.array(df['flux']).reshape(-1,1),np.array(df['model_value']).reshape(-1,1))
print (model.coef_,model.intercept_)