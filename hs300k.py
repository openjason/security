#print('沪深300走势图分析')
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.finance import candlestick2_ohlc
import datetime
data=get_price(['000300.SH'], None, '20171110', '1d', ['open','high','low','close'], True, None, 200, is_panel=0)
data=data['000300.SH']
#时间转化格式
time=data.index
t=[]
for x in time:
    x=str(x).split()[0]
    x=x.split('-')
    x=x[0]+x[1]+x[2]
    x=int(x)
    t.append(x)
#画图数据
time=t
open1=list(data['open'])
high1=list(data['high'])
low1=list(data['low'])
close1=list(data['close'])
#画图
fig,ax = plt.subplots(figsize = (32,8),facecolor='pink')
fig.subplots_adjust() 
plt.xticks()  
plt.yticks()  
plt.title("沪深300K线走势图")  
plt.ylabel("股指")  
ticks = ax.set_xticks(range(1,200,40))
labels = ax.set_xticklabels([time[0],time[40],time[80],time[120],time[160]]) 
candlestick2_ohlc(ax,open1,high1,low1,close1,width=0.6,colorup='red',colordown='green')
#支撑线
plt.plot([75,200],[3316,3954],'g',linewidth=10)
# 红星：回踩1
plt.plot(75, 3316, 'r*', markersize = 40.0,label='趋势线')
plt.annotate(r'二次低位', xy=(75, 3316),
    xycoords='data', xytext=(-90, -50),
    textcoords='offset points', fontsize=26,
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
# 红星：回踩2
plt.plot(140, 3650, 'r*', markersize = 40.0)
plt.annotate(r'止跌，形成趋势线', xy=(140, 3650),
    xycoords='data', xytext=(-90, -50),
    textcoords='offset points', fontsize=26,
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
# 红星：回踩3
plt.plot(172, 3800, 'r*', markersize = 40.0)
plt.annotate(r'回踩趋势线', xy=(172, 3800),
    xycoords='data', xytext=(-90, -50),
    textcoords='offset points', fontsize=26,
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
#MA5
data['ma5']=pd.rolling_mean(data['close'],5)
plt.plot(list(data['ma5']),label='五日均线')
#MA10
data['ma10']=pd.rolling_mean(data['close'],10)
plt.plot(list(data['ma10']),label='十日均线')
#MA20
data['ma20']=pd.rolling_mean(data['close'],20)
plt.plot(list(data['ma20']),label='二十日均线')
#MA30
data['ma30']=pd.rolling_mean(data['close'],30)
plt.plot(list(data['ma30']),label='三十日均线')
#MA60
data['ma60']=pd.rolling_mean(data['close'],60)
plt.plot(list(data['ma60']),label='六十日均线')
plt.legend()
print('沪深300走势图分析')