import pandas as pd

def cal_PWO(dataframe):
    df=dataframe
    dict={}
    slist=[]
    flag=0
    grouped=df['O_N'].groupby(df['O_id'])
    population=grouped.mean().sum()
    S_sum=population
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
        flowrate=(1/s)-(1/S_sum)
        if(flag%1000==0):
            print (i)
        slist.append([O,D,flowrate])
    df1=pd.DataFrame(data=slist,columns=['O_id','D_id','flowrate'])
    df=df.set_index(keys=['O_id','D_id'],drop=False)
    df1 = df1.set_index(keys=['O_id', 'D_id'])
    df['flowrate']=df1['flowrate']

    ##cal the flow
    grouped=df['flowrate'].groupby(df['O_id'])
    flowratesum=grouped.sum()
    slist=[]
    for i, row in df.iterrows():
        O_N=row['O_N']
        D_N=row['D_N']
        O=int(row['O_id'])
        D=int(row['D_id'])
        fowrate=row['flowrate']
        PWO_flux=fowrate*O_N*D_N/(flowratesum[row['O_id']])
        slist.append([O, D, PWO_flux])
    df2 = pd.DataFrame(data=slist, columns=['O_id', 'D_id', 'PWO1_flux'])
    df2 = df2.set_index(keys=['O_id', 'D_id'])
    df['PWO1_flux'] = df2['PWO1_flux']
    scale=df['flux'].mean()/df['PWO1_flux'].mean()
    df['PWO1_flux']=df['PWO1_flux']*scale
    return df
def cal_PWO2(dataframe):
    df=dataframe
    dict={}
    slist=[]
    flag=0
    grouped=df['O_N'].groupby(df['O_id'])
    population=grouped.mean().sum()
    S_sum=population
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
        flowrate=D_N*(((1/s)-(1/S_sum)))
        if(flag%1000==0):
            print (i)
        slist.append([O,D,flowrate])
    df1=pd.DataFrame(data=slist,columns=['O_id','D_id','flowrate'])
    df=df.set_index(keys=['O_id','D_id'],drop=False)
    df1 = df1.set_index(keys=['O_id', 'D_id'])
    df['flowrate']=df1['flowrate']

    ##cal the flow
    grouped=df['flowrate'].groupby(df['O_id'])
    flowratesum=grouped.sum()
    slist=[]
    for i, row in df.iterrows():
        O_N=row['O_N']
        D_N=row['D_N']
        O=int(row['O_id'])
        D=int(row['D_id'])
        fowrate=row['flowrate']

        fluxO=df[df['O_N']==O_N]
        fluxO=fluxO['flux'].sum()
        PWO_flux=fowrate*fluxO/(flowratesum[row['O_id']])
        slist.append([O, D, PWO_flux])
    df2 = pd.DataFrame(data=slist, columns=['O_id', 'D_id', 'PWO_flux'])
    df2 = df2.set_index(keys=['O_id', 'D_id'])
    df['PWO_flux'] = df2['PWO_flux']
    # scale=df['flux'].mean()/df['PWO_flux'].mean()
    # df['PWO_flux']=df['PWO_flux']*scale
    return df

path='D:\\modeldis21_3000_121918+.csv'
df=pd.read_csv(path)
df=cal_PWO2(df)
df.to_csv(path)