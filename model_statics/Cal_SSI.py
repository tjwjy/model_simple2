import pandas as pd
import numpy as np
import math
from scipy.stats import pearsonr,spearmanr
def cal_ssi_fromSeries(series1):
    df_min=series1.min(axis=1)*2
    df_sum=series1.sum(axis=1)
    df_div=df_min/df_sum
    value=df_div.sum()/len(df_div)
    return value

def cal_SSI(path):
    od_dataframe=pd.read_csv(path)
    od_dataframe['flux']+=1
    od_dataframe['model_value_scale']+=1
    od_dataframe['gra_flux']+=1
    series_value=od_dataframe[['model_value_scale','flux']]

    series_preflux=od_dataframe[['gra_flux','flux']]
    print('model SSI is '+str(cal_ssi_fromSeries(series_value)))
    print (pearsonr(od_dataframe['model_value_scale'],od_dataframe['flux']),spearmanr(od_dataframe['model_value_scale'],od_dataframe['flux']))
    print ('gravity model SSI is '+str(cal_ssi_fromSeries(series_preflux)))


    print (pearsonr(od_dataframe['gra_flux'],od_dataframe['flux']),spearmanr(od_dataframe['gra_flux'],od_dataframe['flux']))
    print ('OK')
cal_SSI(r'D:\data_test\shanghai\new\rank\modelR1_30000_rank1.289.csv')