import pandas as pd
import numpy as np
from networkx.algorithms import community
import seaborn as sbn
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
path='D:\\data_test\\test\\od_test\\beijing\\test_results\\0.05\\moedelS_10000_1_0.5.csv'
def dis_func2(dataframe):
    df=dataframe
    dict={}
    slist=[]
    flag=0
    for i,row in df.iterrows():
        flag+=1
        O=row['O_id']
        D=row['D_id']
        dis=row['Dis']
        O_N=row['O_N']
        D_N=row['D_N']
        if(O_N+D_N==0):
            continue
        temp_dfO=df[df['O_id']==O]
        temp_df=temp_dfO[temp_dfO['Dis']<=dis]
        s=temp_df['D_N'].sum()+O_N
        if(flag%1000==0):
            print (i)
        dict[(O,D)]=s
        slist.append([O,D,s])
    df1=pd.DataFrame(data=slist,columns=['O_id','D_id','dis'])
    df=df.set_index(keys=['O_id','D_id'])
    df1 = df1.set_index(keys=['O_id', 'D_id'])
    df['S']=df1['dis']
    df.to_csv('D:\\dis.csv')
    return df
def S_dis_relation(path):
    df=pd.read_csv(path)
    df=df[(df['O_N']!=0)&(df['D_N']!=0)]
    df=df[df['O_id']==39]
    df=dis_func2(df)
    ax=sbn.regplot(x='Dis',y='S',data=df,order=2)
    sbn.regplot(x='Dis', y='S', data=df, order=1,ax=ax)
    df=df[df['Dis']<0.15]
    quadratic_featurize=PolynomialFeatures(degree=2)
    x_square=quadratic_featurize.fit_transform(df['Dis'].values.reshape(-1,1))
    y=df['S'].values
    regression_model=LinearRegression()
    regression_model.fit(x_square,y.reshape(-1,1))
    print('2 r-squared', regression_model.score(x_square, y))
    print(regression_model.coef_)
    regression_model.fit(df['Dis'].values.reshape(-1,1),y.reshape(-1,1))
    print('1 r-squared',regression_model.score(df['Dis'].values.reshape(-1,1), y.reshape(-1,1)))
    plt.show()
df=pd.read_csv(path)
#

S_dis_relation(path)

#
# df=pd.read_csv(path)
# sbn.distplot(df['Dis'],bins=20)
# plt.show()