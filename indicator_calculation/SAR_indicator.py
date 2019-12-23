import pandas as pd
import numpy as np
import datetime

df2=get_price("J2001.XDCE", start_date='2019-1-11', end_date='2019-12-22', frequency='daily',fields=['high','low','close'])
data=df2.dropna()
low=data.loc[:,"low"].values
high=data.loc[:,"high"].values
"""
鉴于talib提供的SAR算法与文化财经等指标算出来的不一致，自己实现了SAR算法，并在joinquant 平台亲自验证
计算结果和文化财经完全一致,可直接复制打joinquant平台验证
"""
class SarData:#存储结构
    af=[]
    ep=[]
    sar=[]
    date=[] 
    
def sar(high,low,up=True,N=4,step=2,mvalue=20):
    step1=step/100
    mvalue1=mvalue/100
    sr_value=SarData() #村总的
    low_pre=999999999 #上一个周期最小值
    high_pre=0 #上一个周期最大值
    for i in range(0,N+1):
        sr_value.ep.append(0)
        sr_value.af.append(0)
        sr_value.sar.append(0) 
    for i in range(N,len(high)):  
        sr_value.ep.append(0)
        sr_value.af.append(0)
        sr_value.sar.append(0) 
        #先确定sr0 
        if up and i==N :#涨势 
            sr_value.ep[i]=min(low[0:N-1])
            sr_value.sar[i]= sr_value.ep[i]
            continue;
        elif up==False and i==N:#跌势 
            sr_value.ep[i]=max(high[0:N-1])
            sr_value.sar[i]= sr_value.ep[i]*-1
            continue; 
             #其他sar计算           
        sr_value.af[i]= sr_value.af[i-1]+step1
        if  sr_value.af[i]>mvalue1:
             sr_value.af[i]=mvalue1
        if up:    
            sr_value.sar[i]=abs(sr_value.sar[i-1])+sr_value.af[i]*(high[i-1]-abs(sr_value.sar[i-1]))
            #转势头
            sr_value.ep[i]=max(sr_value.ep[i-1],high[i])
            high_pre=max(high_pre,high[i])
            #print(i,sr_value.ep[i-1],high[i])
            if low[i]<abs(sr_value.sar[i]):
               #print("转入跌势") 
               up=False
               sr_value.af[i]=0
               low_pre=low[i]
               if low_pre==0:
                   sr_value.sar[i]=max(high[0:i])
               else:
                   sr_value.sar[i]=high_pre*-1   
        else :
            sr_value.sar[i]=(abs(sr_value.sar[i-1])+sr_value.af[i]*(low[i-1]-abs(sr_value.sar[i-1])))
            sr_value.sar[i]=-1*sr_value.sar[i]
            sr_value.ep[i]=min(sr_value.ep[i-1],low[i])
            low_pre=min(low_pre,low[i])
            #print(i,sr_value.ep[i-1],low[i])
            if high[i]>abs(sr_value.sar[i]):
               #print("转入涨势") 
               up=True
               high_pre=high[i] 
               sr_value.af[i]=0
               if high_pre==0:#上涨第一个周期
                    sr_value.sar[i]=min(low[0:i])
               else:   
                   sr_value.sar[i]=low_pre   
    return sr_value.sar
data=sar(high,low,False)
print(data)