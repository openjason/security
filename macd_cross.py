
# -*- coding: utf-8 -*-
"""
test
"""  
import pandas as pd  
import numpy as np  
import datetime  
import time  
#获取数据  
df=pd.read_csv('C:/Users/HXWD/Desktop/rb000.csv',encoding='gbk')  
df.head()
df.columns=['date','open','high','low','close','volume','amt']  
df.head()  
value=[]  
for i in range(5,6):  
    for j in range(20,21):  
        df['ma5']=df['close'].rolling(i).mean()  
        df['ma20']=df['close'].rolling(j).mean()  
        df.ix[df['ma5']>df['ma20'],'cross']=1  
        df.ix[df['ma5']<=df['ma20'],'cross']=-1  
        #df[['close','ma5','ma20']][-200:].plot()  
        df['ret']=(df['close']-df['close'].shift(1))  
        df['profit']=df['ret']*df['cross']  
        #df['profit'].plot()  
        target=df['profit'].sum()  
        s=[i,j,target]  
        ts=time.strftime('%Y-%m-%d %X', time.localtime() )  
        value.append(s)  
        print('当前时间:{}短期参数:{},长期参数:{}优化完毕,净利润{}'.format(ts,i,j,s)) 
data=pd.DataFrame(value)  
#data.to_csv('参数优化.csv')  
#消除趋势后的
df_up=df.cross[df.cross>0]
df_down=df.cross[df.cross<0]
p=len(df_up)/(len(df_down)+len(df_up))
ll=len(df)
mu=p*len(df)
mu
 
import random
suiji_value=[]
for i in range(10000):
    total=[]
    for i in range(len(df)):
        v=random.randint(0,ll)
        if v<mu:
            total.append(1)
        if v>=mu:
            total.append(-1)
    total=pd.Series(total)
    suiji_profit=(df['ret']*total).sum()
    print(suiji_profit)               
    suiji_value.append(suiji_profit)
suiji_value=pd.Series(suiji_value).sum()/10000
suiji_value
#随机信号只能够产生平均83.9的收益，而双均线能够产生15593的利润，
#有理由相信这是一个好策略
#我们尝试消除平均趋势之后再计算相应的盈利
df['new_ret']=(df['close']-df['close'].shift(1))/df['close'].shift(1)
aa=df['new_ret'].mean()
df['new_ret1']=df['new_ret']-pd.Series([aa]*len(df))
df['ret2']=df['new_ret1']*df['close'].shift(1)
(df['ret2']*df['cross']).sum()
#计算出来消除平均趋势之后的收益15571，只差了20多。
#似乎均线策略，马马虎虎证明了，是可以产生预测能力的。
