import pandas as pd
import numpy as np
import math
from matplotlib import pyplot as plt
import seaborn as sbn
from sklearn.linear_model import LinearRegression
def draw_regression(path,attribute,bias):
    colorList = ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074',
             '#546570', '#c4ccd3']
    od_df=pd.read_csv(path)
    # od_df=od_df[od_df['flux1']!=0]
    od_df['flux']+=bias
    od_df[attribute]+=bias

    ##__ draw points of (real,predict) as the background______________________________________________________________
    temp_df=od_df.sample(5000)
    ax=plt.scatter(x=temp_df['flux'],y=temp_df[attribute],c='darkgray',alpha=.5,s=10)

    ##__draw hist with power_law wei_________________________________________________________________________________
    bin_num=20
    min1=0
    interval=math.log(100000,10)
    interval_list=np.linspace(0,interval,bin_num,endpoint=True)
    interval_list2=np.array([math.pow(10,i)+min1 for i in interval_list])
    ##may be wrong

    od_df['tag']=0
    for i in range(bin_num-1,0,-1):
        od_df.loc[od_df['flux']<interval_list2[i],'tag']=interval_list2[i]
    box_value=[np.array(od_df.loc[od_df['tag']==interval,attribute]).tolist() for interval in interval_list2]
    box_position=0.5*(interval_list[1:]+interval_list[:-1])
    box_position=[math.pow(10,i)+min1 for i in box_position]

    bp=plt.boxplot(x=box_value[1:],positions=box_position[0:],widths=[i *.35 for i in interval_list2[1:]],whis=[10,91],sym='')
    for index,box in enumerate(bp['boxes']):
        whisker=bp['whiskers']
        median=bp['medians']
        cap=bp['caps']
        if(np.isnan(box._y).sum()==0):
            if(0 in box._y):
                box.set(color='white',linewidth=1.5)
                cap[index*2].set(color='white', linewidth=1.5)
                cap[index*2+1].set(color='white', linewidth=1.5)
                whisker[index * 2 + 1].set(color='white', linewidth=1.5)
                whisker[index * 2 ].set(color='white', linewidth=1.5)
                median[index].set(color='white', linewidth=1.5)
            else:
                if(box_position[index]>cap[index*2+1]._y[0] or box_position[index]<cap[index*2]._y[0]):
                    # color='orangered'
                    color=colorList[0]
                    box.set(color=color,linewidth=1.5)
                    cap[index*2].set(color=color, linewidth=1.5)
                    cap[index*2+1].set(color=color, linewidth=1.5)
                    whisker[index * 2 + 1].set(color=color, linewidth=1.5)
                    whisker[index * 2 ].set(color=color, linewidth=1.5)
                    median[index].set(color=color, linewidth=1.5)
                else:
                    # color='#009688'
                    color=colorList[1]
                    box.set(color=color,linewidth=1.5)
                    cap[index*2].set(color=color, linewidth=1.5)
                    cap[index*2+1].set(color=color, linewidth=1.5)
                    whisker[index * 2 + 1].set(color=color, linewidth=1.5)
                    whisker[index * 2 ].set(color=color, linewidth=1.5)
                    median[index].set(color=color, linewidth=1.5)


    # for box in bp['boxes']:
    #     box.set(color='royalblue',linewidth=1.5)
    # for cap in bp['caps']:
    #     cap.set(color='royalblue',linewidth=1.5)
    # for whisker in bp['whiskers']:
    #     whisker.set(color='royalblue',linewidth=1.5)
    ##__draw flux's mean and predict mean as point to view the change________________________________________________
    mean_value_list=[]
    for item in interval_list2:
        mean_value_list.append(od_df.loc[od_df['tag']==item,attribute].mean())
    plt.scatter(x=box_position,y=mean_value_list[1:],s=50,c='royalblue')

    # sbn.regplot(x='flux',y=attribute,data=od_df)
    ##__decorate the picture
    plt.plot([1,1000000],[1,1000000],c='black')
    x_array=np.array([i for i in range(10)])
    x_labels=np.array([x_array *pow(10,i) for i in range(1,6)])
    x_labels_array=np.reshape(np.array(x_labels),-1)
    plt.xticks(x_labels_array)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(1,100000)
    plt.ylim(1,100000)
    plt.xlabel('Travels(data)')
    plt.ylabel('Travels(model)')
    plt.savefig('D:\\fig.png',dpi=200)
    plt.show()
draw_regression(r'D:\modelSSh1_3000_31719+.csv',attribute='model_value_scale',bias=1)