import pandas as pd
import sklearn.linear_model as line_model
import math
import numpy as np
import matplotlib.pyplot as plt
def cal_gra_args(path='D:\\data_test\\changsha\\modelR1_3000_rank1.29.csv'):
    temp_path=path
    df=pd.read_csv(temp_path)
    df=df.fillna(0)

    ##__del the flux/ON/DN==0
    df=df[(df['O_N']!=0)&(df['D_N']!=0)&(df['flux']!=0)]
    ##__linear fit the gravity args
    df['flux_OD']=df['flux']/(df['O_N']*df['D_N'])
    df['flux_OD']=df['flux_OD'].apply(math.log)


    model=line_model.LinearRegression()
    model.fit(np.array(df['Dis']).reshape(-1,1),np.array(df['flux_OD']).reshape(-1,1))

    print (model.coef_,model.intercept_)
    model.coef_=model.coef_
    ##__using the args to predict gra_flux
    df2=pd.read_csv(temp_path)
    pre_gravity_flux=model.predict(np.array(df2['Dis']).reshape(-1,1))
    df2['gra_exp_flux']=pre_gravity_flux
    df2['gra_exp_flux']=df2['gra_exp_flux'].apply(lambda x:math.e**x)*df2['D_N']*df2['O_N']
    # df2['gra_flux']=df2['D_N']*df2['O_N']/df2['Dis']**1.87
    ##__out put the predict value and real value describe
    print('gra_flux describe is ')
    print (df2['gra_exp_flux'].describe())
    print('flux describe is ')
    print (df2['flux'].describe())

    df2.to_csv(temp_path)

    print ('OK')

cal_gra_args()